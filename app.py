#!flask/bin/python
from flask import Flask, jsonify, g, session, request
import sqlite3

#IMPORT TEST
import json
from flask import Response

app = Flask(__name__)

DATABASE = 'database.db'

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

users = {
    1: 'paul',
    2: 'mike',
    3: 'robert'
}

## DB & STUFF
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_db():
    cur = get_db().cursor()
    with open('schema.sql', 'r') as schema:
        tmp = schema.read()
    cur.execute(tmp)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# QUERY DB
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# TRAINING
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# @app.route('/users/create/')
#     cur = get_db().cursor()
#     cur.execute()

@app.route('/')
def index():
    # create_db()
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return jsonify({'Hello': 'World'})

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return jsonify({'Login': 'LoL!!'})
    if request.method == 'POST':
        print(request.args['user'])
        # ret = query_db('SELECT * FROM users') 
        # user = query_db('SELECT * FROM users WHERE user = ?',
                # [request.args['user']], one=True)
        var = "%{}%".format(request.args['user'])
        user = query_db('SELECT * FROM users WHERE user LIKE ?',
                [var], one=False)
        print(user)
        # , request.args['user'])
        # print(ret)
        # return Response(json.dumps(ret), mimetype='application/json')
        return 'Hello World'

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user = request.args['username']
        pwd = request.args['password']
        var = "%{}%".format(request.args['user'])
        ret = query_db('SELECT * FROM users WHERE user LIKE ?',
                [var], one=False)




if __name__ == '__main__':
    app.run(debug=True)