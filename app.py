from flask import Flask, render_template, redirect, url_for, request
# from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.habitLog
habits = db.habits

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', habits=habits.find())

@app.route('/habits/new')
def habits_new():
    return render_template('habit_new.html')

@app.route('/habits', methods=['POST'])
def habits_submit():
    habit = {
        'name': request.form.get('name'),
    }
    habits.insert_one(habit)
    print(habits)
    return redirect(url_for('.index'))

if __name__ == '__main__':
    app.run(debug=True)