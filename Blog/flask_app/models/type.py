from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import html


class Type:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.img_url = data['img_url']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM post_types;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query)
        # Create an empty list to append our instances of friends
        post_types = []
        # Iterate over the db results and create instances of friends with cls.
        for post_type in results:
            post_types.append( cls(post_type) )
        return post_types

    @classmethod
    def save(cls, data):
        query = "INSERT INTO post_types ( name, img_url, description, created_at, updated_at) VALUES ( %(name)s, %(img_url)s, %(description)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('blog').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM post_types WHERE id=%(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('blog').query_db( query, data )

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM post_types WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('blog').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])



