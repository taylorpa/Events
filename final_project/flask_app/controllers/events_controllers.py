from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.event import Event
from flask_app.models.user import User


@app.route('/new/event')
def new_event():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("new_event.html", user=User.get_by_id(data))

@app.route('/create/event', methods=['POST'])
def create_event():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/new/event')
        
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "location": request.form["location"],
        "date": request.form["date"],
        "time": request.form["time"],
        "price": float(request.form["price"]),
        "display": int(request.form["display"]),
        "user_id": session["user_id"]
    }
    Event.save(data)
    
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("edit_event.html", edit=Event.get_one(data), user=User.get_by_id(user_data))
    

@app.route('/update/event/<int:id>',methods=['POST'])
def update_event(id):
  
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "location": request.form["location"],
        "date": request.form["date"],
        "time": request.form["time"],
        "price": float(request.form["price"]),
        "display": int(request.form["display"]),
        "id": request.form['id']
    }

    
    if not Event.validate_event(data):
        return redirect(f'/edit/{id}')
    
    Event.update(data)
    return redirect('/dashboard')

    
@app.route('/show/<int:id>') 
def show_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    this_user_id = {
        session['user_id']
    }   
    event_data = {
        "id" : id
    }     
    data = {
        "id" : this_user_id
        }    

    this_user_id = User.get_by_id(data)
    this_event = Event.get_event_with_creator(event_data)
    return render_template("show.html", event = this_event, user = this_user_id)



@app.route('/destroy/event/<int:id>')
def destroy_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Event.destroy(data)
    return redirect('/dashboard')


