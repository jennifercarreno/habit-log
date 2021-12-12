import re
from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.lifeLog
habits = db.habits
tasks = db.tasks
app = Flask(__name__)

def top_habits():
    global top_habit
    global third_habit
    global second_habit
    top_number = 0
    second_number = 0
    third_number = 0

    top_habit = "None"
    second_habit = "None"
    third_habit = "None"
    for habit in habits.find():
        
        for habit in habits.find():
            # print(habit['count'])
            # print(habit)
            if habit['count'] > top_number:
                top_number = habit['count']
                top_habit = habit['name']
                # print(f"top habit: {top_habit}")
                # print(f"top number: {top_number}")
                # print("first if done")

            if habit['count'] < top_number and habit['count'] > second_number:
                second_number = habit['count']
                second_habit = habit['name']
                # print(f"second number: {second_number}")
                # print(f"secong habit: {second_habit}")
                # print("second if done")

            if habit['count'] < second_number and habit['count'] > third_number:
                third_number = habit['count']
                third_habit = habit['name']
                # print(f"third number: {third_number}")
                print(f"third habit: {third_habit}")
                # print("third if done")

            if third_habit == 'none': 
                print('----')
        
       
        
    # print("one round done")
    return(top_habit, second_habit, third_habit)

def mondaySum():
    monday_logs =[]
    for habit in habits.find():
        monday_count = habit.get('monday')
        if monday_count == '✅':
            monday_logs.append(monday_count)
    count = len(monday_logs)
    # print(monday_logs)
    return str(count)

def tuesdaySum():
    tuesday_logs =[]
    for habit in habits.find():
        tuesday_count = habit.get('tuesday')
        if tuesday_count == '✅':
            tuesday_logs.append(tuesday_count)
    count = len(tuesday_logs)
    # print(tuesday_logs)
    return str(count)

def thursdaySum():
    thursday_logs =[]
    for habit in habits.find():
        thursday_count = habit.get('thursday')
        if thursday_count == '✅':
            thursday_logs.append(thursday_count)
    count = len(thursday_logs)
    # print(thursday_logs)
    return str(count)

def wednesdaySum():
    wednesday_logs =[]
    for habit in habits.find():
        wednesday_count = habit.get('wednesday')
        if wednesday_count == '✅':
            wednesday_logs.append(wednesday_count)
    count = len(wednesday_logs)
    # print(wednesday_logs)
    return str(count)

def fridaySum():
    friday_logs =[]
    for habit in habits.find():
        friday_count = habit.get('friday')
        if friday_count == '✅':
            friday_logs.append(friday_count)
    count = len(friday_logs)
    # print(friday_logs)
    return str(count)

def saturdaySum():
    saturday_logs =[]
    for habit in habits.find():
        saturday_count = habit.get('saturday')
        if saturday_count == '✅':
            saturday_logs.append(saturday_count)
    count = len(saturday_logs)
    # print(saturday_logs)
    return str(count)

def sundaySum():
    sunday_logs =[]
    for habit in habits.find():
        sunday_count = habit.get('sunday')
        if sunday_count == '✅':
            sunday_logs.append(sunday_count)
    count = len(sunday_logs)
    # print(sunday_logs)
    return str(count)

def complete_habits():
    total = 0
    habit_total = 0
    for habit in habits.find():
        habit_total += habit['count']
        total += 1

    percent_complete = (habit_total / (total * 7)) * 100
    complete = f"{habit_total} / {total * 7}"
    # print(total)
    # print('habit_total')
    return(f"{round(percent_complete, 2)}%", complete)

def average_habits():
    habit_sum = 0
    count = 0
    for habit in habits.find():
        habit_sum += habit["count"]
        count += 1
    average = habit_sum / count
    return(round(average, 2))

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
    return render_template('home.html', habits=habits.find(), monday_count = monday_count, tuesday_count = tuesday_count, wednesday_count = wednesday_count, thursday_count = thursday_count, friday_count = friday_count, saturday_count = saturday_count, sunday_count = sunday_count, tasks=tasks.find())

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
        'sunday': request.form.get('sunday'),
        'count': 0
    }
        
    if habit["monday"] != '✅':
        habit['monday'] = '❌'
    else:
        habit['count'] += 1
    if habit['tuesday'] != '✅':
        habit["tuesday"] = '❌'
    else:
        habit['count'] += 1
    if habit['wednesday'] != '✅':
        habit['wednesday'] = '❌'
    else:
        habit['count'] += 1
    if habit['thursday'] != '✅':
        habit["thursday"] = '❌'
    else:
        habit['count'] += 1
    if habit["friday"] != '✅':
        habit['friday'] = '❌'
    else:
        habit['count'] += 1
    if habit['saturday'] != '✅':
        habit["saturday"] = '❌'
    else:
        habit['count'] += 1
    if habit["sunday"] != '✅':
        habit['sunday'] = '❌'
    else:
        habit['count'] += 1
    print(habits.find_one('monday'))
    habits.insert_one(habit)
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
        'sunday': request.form.get('sunday'),
        'count': 0

    }
    if updated_habit["monday"] != '✅':
        updated_habit['monday'] = '❌'
    else:
        updated_habit['count'] += 1
    if updated_habit['tuesday'] != '✅':
        updated_habit["tuesday"] = '❌'
    else:
        updated_habit['count'] += 1
    if updated_habit['wednesday'] != '✅':
        updated_habit['wednesday'] = '❌'
    else:
        updated_habit['count'] += 1
    if updated_habit['thursday'] != '✅':
        updated_habit["thursday"] = '❌'
    else:
        updated_habit['count'] += 1
    if updated_habit["friday"] != '✅':
        updated_habit['friday'] = '❌'
    else:
        updated_habit['count'] += 1
    if updated_habit['saturday'] != '✅':
        updated_habit["saturday"] = '❌'
    else:
        updated_habit['count'] += 1
    if updated_habit["sunday"] != '✅':
        updated_habit['sunday'] = '❌'
    else:
        updated_habit['count'] += 1
    # set the former playlist to the new one we just updated/edited
    habits.update_one(
        {'_id': ObjectId(habit_id)},
        {'$set': updated_habit})
    # take us back to the playlist's show page
    return redirect(url_for('index'))

#display stats page
@app.route('/habits/stats')
def habits_stats():

    top_one_habits = top_habits()[0]
    top_second_habit = top_habits()[1]
    top_third_habit = top_habits()[2]
    complate_habit  = complete_habits()[0]
    complete_tally = complete_habits()[1]
    average_habit_count = average_habits()
    return render_template('stats.html', top_one_habits=top_one_habits, top_second_habit = top_second_habit, top_third_habit = top_third_habit, complate_habit = complate_habit, complete_tally = complete_tally, average_habit_count = average_habit_count)

@app.route('/', methods=['POST'])
def post_todos():
    task = {
        'name': request.form.get('content')
    }
    tasks.insert_one(task)
    return redirect(url_for('.index'))

if __name__ == '__main__':
    app.run(debug=True)