from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.habitLog
habits = db.habits

app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('home.html', habits=habits.find())

# prompts to create a new habit
@app.route('/habits/new')
def habits_new():
    return render_template('habit_new.html')

# displays new habit on log
@app.route('/habits', methods=['POST'])
def habits_submit():
    habit = {
        'name': request.form.get('name'),
    }
    habits.insert_one(habit)
    print(habits)
    return redirect(url_for('.index'))

# deletes a habit
@app.route('/habits/<habit_id>/delete', methods=['POST'])
def habits_delete(habit_id):
    habits.delete_one({'_id': ObjectId(habit_id)})
    return redirect(url_for('index'))

# edit a habit
@app.route('/habits/<habit_id>/edit')
def habits_edit(habit_id):
    habit = habits.find_one({'_id': ObjectId(habit_id)})
    return render_template('habit_edit.html', habit=habit)

# update a habit
@app.route('/habits/<habit_id>', methods=['POST'])
def habits_update(habit_id):
    updated_habit = {
        'name': request.form.get('name'),
    }
    # set the former playlist to the new one we just updated/edited
    habits.update_one(
        {'_id': ObjectId(habit_id)},
        {'$set': updated_habit})
    # take us back to the playlist's show page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)