import re
from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.habitLog
habits = db.habits

app = Flask(__name__)

def blank():
    for habit in habits.find():
        habit_check = habit.get('monday')
        if habit_check == '':
            habit = {'monday': "pee"}
            print("found unchecked")
    
    return

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
        'monday': request.form.get('monday'),
        'tuesday': request.form.get('tuesday'),
        'wednesday': request.form.get('wednesday'),
        'thursday':request.form.get('thursday'),
        'friday': request.form.get('friday'),
        'saturday': request.form.get('saturday'),
        'sunday': request.form.get('sunday')
    }
    
    # blank()

    # if habit.get('monday') == '':
    #     habit.monday = ''
    # if habits.find_one('tuesday') == 'None':
    #     habit['tuesday'] = ''
    # if habits.find_one('wednesday') == 'None':
    #     habit['wednesday'] = ''
    # if habits.find_one('thursday') == 'None':
    #     habit['thursday'] = ''
    # if habits.find_one('friday') == 'None':
    #     habit['friday'] = ''
    # if habits.find_one('saturday') == 'None':
    #     habit['saturday'] = ''
    # if habits.find_one('sunday') == 'None':
    #     habit['sunday'] = ''
    
    habits.insert_one(habit)

    print(habits.find_one('monday'))
    # print(habit['monday'].value)
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