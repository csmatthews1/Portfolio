from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import post
from flask import flash

class Comment:
    def __init__( self , data ):
        tempData = {
            'id': data['author_id']
        }
        self.id = data['id']
        self.comment = data['comment']
        self.author = user.User.get_by_id(tempData)
        tempData['id'] = data['post_id']
        self.post = post.Post.get_by_id(tempData)
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query)
        # Create an empty list to append our instances of comments
        comments = []
        # Iterate over the db results and create instances of comments with cls.
        for comment in results:
            comments.append( cls(comment) )
        return comments

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('blog').query_db(query, data)
        if len(result) < 1 or result == False:
            return False
            
        return cls(result[0])

    @classmethod
    def get_by_post(cls, data):
        query = "SELECT * FROM comments WHERE post_id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        # Create an empty list to append our instances of comments
        comments = []
        if results == False:
            return comments
            
        # Iterate over the db results and create instances of comments with cls.
        for comment in results:
            comments.append( cls(comment) )
        return comments

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments ( post_id, author_id, comment, created_at, updated_at) VALUES ( %(post_id)s, %(author_id)s, %(comment)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('blog').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comments WHERE id=%(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('blog').query_db( query, data )




