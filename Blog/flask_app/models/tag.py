from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import html


class Tag:
    def __init__( self , data ):
        self.id = data['id']
        self.tag = data['tag']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tags;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query)
        # Create an empty list to append our instances of friends
        tags = []
        # Iterate over the db results and create instances of friends with cls.
        for tag in results:
            tags.append( cls(tag) )
        return tags
    
    @classmethod
    def delete(cls, data):
        #delete associations with posts for this tag
        query = "DELETE FROM associations WHERE tag_id=%(id)s;"
        connectToMySQL('blog').query_db( query, data )

        # delete tag in table
        query = "DELETE FROM tags WHERE id=%(id)s;"
        return connectToMySQL('blog').query_db( query, data )

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tags ( tag, created_at, updated_at) VALUES ( %(tag)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('blog').query_db( query, data )

