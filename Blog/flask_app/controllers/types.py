from flask_app import app
from flask import Flask,render_template, redirect, request
from flask_app.models.post import Post
from flask_app.models.type import Type
from flask_bcrypt import Bcrypt
from flask import flash

@app.route('/managetypes')         
def types():
    types = Type.get_all()

    return render_template("types.html", types = types)


@app.route('/deletetype/<int:id>')         
def deletetype(id):
    data = {
        'id': id
    }
    posts = Post.get_all()
    numPostsOfType = 0

    for p in posts:
        if p.type_id == id:
            numPostsOfType += 1
    
    if numPostsOfType > 0:
        type = Type.get_by_id(data)
        flash(f"Cannot delete {type.name}.  {numPostsOfType} post(s) exist of that type.")
        return redirect("/managetypes")

    Type.delete(data)
    return redirect("/managetypes")

@app.route('/addtype', methods=['POST'])         
def addtype():
    data = {
        'name': request.form['name'],
        'img_url': request.form['img_url'],
        'description': request.form['description']
    }
    Type.save(data)
    return redirect("/managetypes")