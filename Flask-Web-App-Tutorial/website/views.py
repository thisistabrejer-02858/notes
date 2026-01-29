from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route("/edit-note", methods=["POST"])
@login_required
def edit_note():
    data = json.loads(request.data)
    note_id = data.get("noteId")
    new_text = data.get("text")

    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        note.data = new_text
        db.session.commit()

    return jsonify({"success": True})

@views.route("/add-note", methods=["POST"])
@login_required
def add_note():
    data = json.loads(request.data)
    note_text = data.get("note")

    if note_text:
        note = Note(data=note_text, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()

    return jsonify({"success": True})
