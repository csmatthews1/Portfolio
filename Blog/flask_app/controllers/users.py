from flask_app import app
from flask import Flask,render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.type import Type
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')         
def index():
    carousel = []
    posts = Post.get_all()
    post_types = Type.get_all()
    for p in posts:
        if (int(p.top_post)):
            carousel.append(p)
    data = {
        'num': 5
    }
    archive = Post.build_archive()
    posts = Post.get_recent(data)
    return render_template("index.html", posts = posts, post_types = post_types, carousel = carousel, archive = archive)
    
@app.route('/signin')         
def signin():
    return render_template('login.html')

@app.route('/register', methods=['POST'])         
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'img_url': "{{ url_for('static', filename='img/user.png') }}",
        'admin': 0,
        'subscribed': 0
    }

    session['user_id'] = User.save(data)
    session['admin'] = 0
    return redirect("/")
    
@app.route('/login', methods=['POST'])         
def login():
    if not User.validate_login(request.form):
        return redirect('/signin')

    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Incorrect/unregistered Email and Password", "login")
        return redirect ('/signin')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Incorrect/unregistered Email and Password", "login")
        return redirect ('/signin')

    session['user_id'] = user_in_db.id
    session['admin'] = user_in_db.admin
    return redirect("/")
    
@app.route('/logout')         
def goback():
    session.clear()
    return redirect('/')

@app.route('/delete/<int:id>')         
def delete_user(id):
    data = {
        'id': id
    }
    User.delete(data)
    return redirect('/manageusers')

@app.route('/changeadmin/<int:id>')         
def change_admin(id):
    data = {
        'id': id
    }
    u = User.get_by_id(data)

    if (u.admin):
        data['admin'] = 0
    else:
        data['admin'] = 1
    

    User.update_admin(data)
    return redirect('/manageusers')
