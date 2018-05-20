#!flask/bin/python
from flask import Flask, jsonify, g, session, request
import sqlite3

#IMPORT TEST
import json
from flask import Response

app = Flask(__name__)

DATABASE = 'database.db'

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

def insertUser(username,password):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (user,pass) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

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

# LOGIN ROUTE
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return jsonify({'Login': 'LoL!!'})
    if request.method == 'POST':
        var = "%{}%".format(request.args['username'])
        user = query_db('SELECT * FROM users WHERE user = ?',
                [var], one=False)
        print(user)
        # return Response(json.dumps(ret), mimetype='application/json')
        return 'Hello World'

# REGISTER ROUTE
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return jsonify({'Login': 'LoL!!'})

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # var = "%{}%".format(request.form.get('username'))
        var = (username, password,)
        user = query_db('SELECT * FROM users WHERE user = ?',
                [username], one=True)
        if user is None:
            insertUser(username,password)
            print('INSERT')
        else:
            return 'NON !'
            print('TEST = FALSE')

        # print(test)

        return jsonify({username: password})
        # pwd = request.args['password']
        # usr = "%{}%".format(request.args['user'])
        # pwd = "%{}%".format(request.args['password'])
        # ret = query_db('SELECT * FROM users WHERE user LIKE ?',
                # [var], one=False)
        return 'Hello Zorg!'



if __name__ == '__main__':
    app.run(debug=True)