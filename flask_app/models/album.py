from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, redirect
from flask_app.models.login import Login
from flask_app import DATABASE

class Album:
    def __init__(self, data):
        self.id = data['id']
        self.album_id = data['album_id']
        self.rating = data['rating']
        self.registration_id = data['registration_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM albums;"
        results = connectToMySQL(DATABASE).query_db(query)

        users = []

        for row in results:
            users.append( cls(row) )
        return users

    @classmethod
    def insert(cls, data):
        query = "INSERT INTO albums (album_id, rating, registration_id, created_at, updated_at) VALUES (%(album_id)s,%(rating)s,%(registration_id)s, now(), now());"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def edit(cls, data):
        
        query = "UPDATE albums SET rating = %(rating)s, updated_at = now() WHERE registration_id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE from albums WHERE album_id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_id(cls, data):

        query = "SELECT * FROM albums where registration_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        users = []

        for row in results:
            users.append( cls(row) )
        return users


    @classmethod
    def get_login_with_sighting( cls ):
        query = "SELECT * FROM albums LEFT JOIN registration ON albums.registration_id = registration.id;"
        results = connectToMySQL(DATABASE).query_db( query )
        print(results[0])
        # login = cls( results[0] )
        list_of_albums = []
        
        for row_from_db in results:
            album = cls(row_from_db)
            login_data = {
                "id" : row_from_db["registration.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "password" : row_from_db["password"],
                "created_at" : row_from_db["registration.created_at"],
                "updated_at" : row_from_db["registration.updated_at"]
            }
            login = Login(login_data)
            album.login = login
            list_of_albums.append(album)
            # login.sightings.append( sasquatch.Sasquatch( login_data ) )
        return list_of_albums
        