from flask_app import app
from flask import Flask,render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.type import Type
from flask_app.models.comment import Comment
from flask import flash
import calendar


@app.route('/manageusers')         
def users():
    users = User.get_all()
    return render_template("users.html", users = users)

@app.route('/admin')         
def admin():
    return render_template("compose.html")

@app.route('/managecomments')         
def comments():
    return render_template("comments.html")

@app.route('/selecttop')         
def top():
    posts = Post.get_all()
    return render_template("top.html", posts = posts)

@app.route('/viewpost/<int:id>')         
def viewpost(id):
    data = {
        'id': id
    }
    post = Post.get_by_id(data)
    comments = Comment.get_by_post(data)
    return render_template("view_post.html", post = post, comments =comments)

@app.route('/showtype/<int:id>')         
def showtype(id):
    data = {
        'id': id,
        'type_id': id
    }
    post_type = Type.get_by_id(data)
    posts = Post.get_by_type(data)
    title = "Showing " + str(len(posts)) + " " + post_type.name + " post(s)."

    return render_template("view_results.html", resultsTitle = title, posts = posts)

@app.route('/showmonth/<int:month>/<int:year>')         
def showmonth(month, year):
    data = {
        'month': month,
        'year': year
    }

    posts = Post.get_by_month(data)
    title = "Showing " + str(len(posts)) + " post(s) from " + calendar.month_name[month] + " " + str(year) + "."

    return render_template("view_results.html", resultsTitle = title, posts = posts)

@app.route('/searchposts', methods=['POST'])         
def searchposts():
    data = {
        'searchString': '%%' + request.form['searchString'] + '%%'
    }
    if request.form['search_by'] == "1":
        posts = Post.search_by_title(data)
        searchBy = "the title"

    elif request.form['search_by'] == "2":
        posts = Post.search_by_author(data)
        searchBy = "th author"
    else:
        posts = Post.search_by_content(data)
        searchBy = "the content"

    title = "Showing " + str(len(posts)) + " post(s) containing \"" + request.form['searchString'] + "\" in " + searchBy + "."

    return render_template("view_results.html", resultsTitle = title, posts = posts)

@app.route('/updatetop', methods=['POST'])         
def updatetop():
    data = {
        'id': 0,
        'top_post': 0
    }
    posts = Post.get_all()
    for p in posts:
        data['top_post'] = 0
        data['id'] = p.id
        if ('top_post'+str(p.id)) in request.form:
            data['top_post'] = 1
        Post.update_top(data)   

    posts = Post.get_all()
    return render_template("top.html", posts = posts)

@app.route('/newpost', methods=['POST'])         
def newpost():
    if session.get('_flashes') == True:
        session['_flashes'].clear()

    if not Post.validate(request.form):
        return redirect('/admin')

    data = {
        'type_id': request.form['type_id'],
        'title': request.form['title'],
        'abstract': request.form['abstract'],
        'body': request.form['body'],
        'author_name': request.form['author_name'],
        'author_title': request.form['author_title'],
        'highlight_img': request.form['highlight_img'],
        'highlight_url': request.form['highlight_url'],
        'top_post': 0
    }

    Post.save(data)
    flash("Post successfully submitted.")
    return redirect("/admin")

@app.route('/submitcomment', methods=['POST'])         
def submitcomment():
    if len(request.form['comment']) < 1:
        return redirect("/viewpost/" + request.form['id'])
    
    data = {
        'post_id': request.form['id'],
        'comment': request.form['comment'],
        'author_id': session['user_id'],
    }

    Comment.save(data)
    return redirect("/viewpost/" + request.form['id'])

@app.route('/deletecomment/<int:post_id>/<int:id>')         
def deletecomment(post_id, id):
    data = {
        'id': id
    }
    Comment.delete(data)
    return redirect("/viewpost/" + str(post_id))

