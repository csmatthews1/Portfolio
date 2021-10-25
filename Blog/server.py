from flask_app import app
from flask_app.controllers import users, posts, tags, types

if __name__=="__main__":   
    app.run(debug=True)   