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

def mondaySum():
    monday_logs =[]
    for habit in habits.find():
        monday_count = habit.get('monday')
        if monday_count == '☑':
            monday_logs.append(monday_count)
    count = len(monday_logs)
    print(monday_logs)
    return str(count)

def tuesdaySum():
    tuesday_logs =[]
    for habit in habits.find():
        tuesday_count = habit.get('tuesday')
        if tuesday_count == '☑':
            tuesday_logs.append(tuesday_count)
    count = len(tuesday_logs)
    print(tuesday_logs)
    return str(count)

def thursdaySum():
    thursday_logs =[]
    for habit in habits.find():
        thursday_count = habit.get('thursday')
        if thursday_count == '☑':
            thursday_logs.append(thursday_count)
    count = len(thursday_logs)
    print(thursday_logs)
    return str(count)

def wednesdaySum():
    wednesday_logs =[]
    for habit in habits.find():
        wednesday_count = habit.get('wednesday')
        if wednesday_count == '☑':
            wednesday_logs.append(wednesday_count)
    count = len(wednesday_logs)
    print(wednesday_logs)
    return str(count)

def fridaySum():
    friday_logs =[]
    for habit in habits.find():
        friday_count = habit.get('friday')
        if friday_count == '☑':
            friday_logs.append(friday_count)
    count = len(friday_logs)
    print(friday_logs)
    return str(count)

def saturdaySum():
    saturday_logs =[]
    for habit in habits.find():
        saturday_count = habit.get('saturday')
        if saturday_count == '☑':
            saturday_logs.append(saturday_count)
    count = len(saturday_logs)
    print(saturday_logs)
    return str(count)

def sundaySum():
    sunday_logs =[]
    for habit in habits.find():
        sunday_count = habit.get('sunday')
        if sunday_count == '☑':
            sunday_logs.append(sunday_count)
    count = len(sunday_logs)
    print(sunday_logs)
    return str(count)

# home page
@app.route('/')
def index():
    monday_count = mondaySum()
    tuesday_count = tuesdaySum()
    wednesday_count = wednesdaySum()
    thursday_count = thursdaySum()
    friday_count = fridaySum()
    saturday_count = saturdaySum()
    sunday_count = sundaySum()

    return render_template('home.html', habits=habits.find(), monday_count = monday_count, tuesday_count = tuesday_count, wednesday_count = wednesday_count, thursday_count = thursday_count, friday_count = friday_count, saturday_count = saturday_count, sunday_count = sunday_count)

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
        'monday': request.form.get('monday'),
        'tuesday': request.form.get('tuesday'),
        'wednesday': request.form.get('wednesday'),
        'thursday':request.form.get('thursday'),
        'friday': request.form.get('friday'),
        'saturday': request.form.get('saturday'),
        'sunday': request.form.get('sunday')
    }
    # set the former playlist to the new one we just updated/edited
    habits.update_one(
        {'_id': ObjectId(habit_id)},
        {'$set': updated_habit})
    # take us back to the playlist's show page
    return redirect(url_for('index'))

@app.route('/habits/stats')
def habits_stats():
    return render_template('stats.html')
if __name__ == '__main__':
    app.run(debug=True)