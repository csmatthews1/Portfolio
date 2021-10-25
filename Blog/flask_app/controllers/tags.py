from flask_app import app
from flask import Flask,render_template, redirect, request, session
from flask_app.models.post import Post
from flask_app.models.tag import Tag
from flask import flash
import flask

@app.route('/managetags')         
def managetags():
    tags = Tag.get_all()
    return render_template("tags.html", tags = tags)

@app.route('/deletetag/<int:id>')         
def deletetag(id):
    data = {
        'id': id
    }

    Tag.delete(data)
    return redirect("/managetags")

@app.route('/addtag', methods=['POST'])         
def addtag():
    data = {
        'tag': request.form['tag']
    }
    Tag.save(data)
    return redirect("/managetags")