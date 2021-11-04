from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.comment import Comment
from flask import flash
import calendar

class Post:
    def __init__( self , data ):
        self.id = data['id']
        self.type_id = data['type_id']
        self.title = data['title']
        self.abstract = data['abstract']
        self.body = data['body']
        self.author_name = data['author_name']
        self.author_title = data['author_title']
        self.highlight_img = data['highlight_img']
        self.highlight_url = data['highlight_url']
        self.top_post = data['top_post']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.likedUsers = [];
        query = "SELECT user_id FROM likes WHERE post_id = %(id)s;"
        results = connectToMySQL('blog').query_db(query, data)
        likes = []
        # Iterate over the db results and create instances of friends with cls.
        for like in results:
            self.likedUsers.append( like['user_id'] )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query)
        # Create an empty list to append our instances of friends
        posts = []
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('blog').query_db(query, data)
        if len(result) < 1 or result == False:
            return False
            
        return cls(result[0])

    @classmethod
    def get_by_type(cls, data):
        query = "SELECT * FROM posts WHERE type_id = %(type_id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        posts = []
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def get_by_month(cls, data):
        query = "SELECT * FROM posts WHERE MONTH(created_at) = %(month)s AND YEAR(created_at)=%(year)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        posts = []
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def search_by_title(cls, data):
        query = "SELECT * FROM posts WHERE UPPER(title) LIKE UPPER(%(searchString)s);"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        posts = []
        if results == False:
            return posts
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def search_by_author(cls, data):
        query = "SELECT * FROM posts WHERE UPPER(author_name) LIKE UPPER(%(searchString)s);"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        posts = []
        if results == False:
            return posts
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def search_by_content(cls, data):
        query = "SELECT * FROM posts WHERE UPPER(abstract) LIKE UPPER(%(searchString)s) OR UPPER(body) LIKE UPPER(%(searchString)s);"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        posts = []
        if results == False:
            return posts
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def get_recent(cls, data):
        query = "SELECT * FROM posts ORDER BY id DESC LIMIT %(num)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('blog').query_db(query, data)
        # Create an empty list to append our instances of friends
        posts = []
        # Iterate over the db results and create instances of friends with cls.
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts ( type_id, title, abstract, body, author_name, author_title, highlight_img, highlight_url, top_post, created_at, updated_at) VALUES ( %(type_id)s, %(title)s, %(abstract)s, %(body)s, %(author_name)s, %(author_title)s, %(highlight_img)s, %(highlight_url)s, %(top_post)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('blog').query_db( query, data )

    @classmethod
    def update_top(cls, data):
        query = "UPDATE posts SET top_post = %(top_post)s WHERE id=%(id)s"

        return connectToMySQL('blog').query_db( query, data )

    @classmethod
    def toggleLike(cls, data):
        if data['liked'] != "0":
            query = "DELETE FROM likes WHERE post_id=%(post_id)s AND user_id=%(user_id)s;"
            return connectToMySQL('blog').query_db( query, data )
        else:
            query = "INSERT INTO likes ( post_id, user_id, created_at, updated_at ) VALUES ( %(post_id)s, %(user_id)s, NOW(), NOW());"
            return connectToMySQL('blog').query_db( query, data )


    @staticmethod
    def validate(post):
        is_valid = True;
        if post['type_id'] == "Select...": 
            flash("You must select a post type.")
            is_valid = False      
        if len(post['title']) < 8:
            flash("Title must be at least 8 characters")
            is_valid = False      
        if len(post['body']) < 10:
            flash("Body must be at least 10 characters.")
            is_valid = False       
        return is_valid

    @staticmethod
    def build_archive():
        query = "SELECT MONTH(created_at) AS Created_Month, YEAR(created_at) AS Created_Year, COUNT(id) AS Post_Count FROM blog.posts GROUP BY MONTH(created_at), YEAR(created_at);"

        results = connectToMySQL('blog').query_db(query)

        monthData = []
        for row in results:
            row['Month_Name'] = calendar.month_name[row['Created_Month']]
            monthData.append(row)

        return monthData
            

