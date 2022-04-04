from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Event:  
    
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.date = data['date']
        self.time = data['time']
        self.price = data['price']
        self.display = data['display']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = []
        self.sellers = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO events (title, description, location, date, time, price, display, user_id) VALUES (%(title)s,%(description)s, %(location)s, %(date)s, %(time)s, %(price)s, %(display)s,%(user_id)s);"
        return connectToMySQL('events_schema').query_db(query, data)
       

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM events;'
        results =  connectToMySQL('events_schema').query_db(query)
        all_events = []
        for row in results:
            print(row['title'])
            all_events.append( cls(row) )
        return all_events
        
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL('events_schema').query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET , title=%(title)s, description=%(description)s, location = %(location)s, date=%(date)s, time=%(time)s, price=%(price)s, display=%(display)s updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('events_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL('events_schema').query_db(query,data)

    @classmethod
    def get_event_with_creator(cls, data):
        
        query = 'SELECT * FROM events JOIN users ON users.id = events.user_id WHERE events.id = %(id)s;'
        results = connectToMySQL('events_schema').query_db(query, data)
        
        all_events = []
        for row in results:
            events_user_data = cls(row)
            userData = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            
            events_user_data.creator = User(userData)
       
            all_events.append(events_user_data)
        return all_events

    @staticmethod
    def validate_event(event):
        is_valid = True
        if len(event['title']) < 1:
            is_valid = False
            flash("Title is required","event")
        if len(event['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","event")
        if len(event['location']) < 1:
            is_valid = False
            flash("Location is required","event") 
        if event['date'] == "":
            is_valid = False
            flash("Please enter a date", "event")
        if event['price'] == "":
            is_valid = False
            flash("Price must have a value","event")
        elif float(event['price']) == 0:
            is_valid = False
            flash("Price must be great than 0","event")
        return is_valid
