import mysql.connector
from dotenv import load_dotenv
import os
import datetime
from hashlib import sha256
import requests
import time
from flask import Flask,render_template,redirect,request,jsonify
from main import *
from random import randint

app = Flask(__name__)

global user#Je le met la pour que la auth se remette pas a False dès qu'ont reviens à '/' parcontre il faut donc faire une ile pour logout ! Laisse le içi jte jure c'est mieux
user = User()

@app.route('/', methods=['GET'])
def render_logout():
    if user.auth == True:
        return redirect(f'/user/{user.name}')
    return render_template('home.html')


@app.route('/register',methods=['GET', 'POST'])
def render_register():
    global user
    special_characters = "!@#$%^&*()-+?_=,<>/"
    numeros="1234567890"
    maj="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if request.method=='POST':
        name=request.form['username']
        pwd=request.form['Password']
        pwd_confirm=request.form['Confirm Password']
        if pwd==pwd_confirm and any(car in special_characters for car in pwd) and any(num in numeros for num in pwd) and any(upper in maj for upper in pwd):
            user.signup(name,pwd)
            return redirect(f'/user/{user.name}')
        else:return render_register()
    else:return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    global user
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['password']

        user.login(name, pwd)
        if user.auth:
            user.spawn_island()  # Appelle la méthode spawn_island lorsque l'utilisateur se connecte
            return redirect(f'/user/{user.name}')
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/user/<username>', methods=['GET'])
def auth_required(username):
    if user.auth:
        return render_profile(username)
    else:
        return redirect('/')

def render_profile(username):
    if username == user.name:
        islands = user.spawn_island()  
        return render_template('index.html', islands=islands)
    else:
        all_users = Query()
        all_users.send_query(Query.query_accountslist, None)
        liste = all_users.cursor.fetchall()
        for i in liste:
            if i[0] == username:
                return render_template('other_profile.html', profile=username, username=user.name)
        return render_template('not_found.html', url=username, username=user.name)

@app.route('/chat/<int:island_id>', methods=['GET'])
def yourconv_required(island_id):
    if island_id in user.chat_id():
        return chat(island_id)
    else:
        return render_template('pb_chat.html')
def chat(island_id):
    
    return render_template('chat.html', chat=user.join_chat(island_id))

@app.route('/send-message', methods=['POST'])
def send_chat():
    try:
        message_data = request.json
        text = message_data.get('message')
        
        temps = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        val = (user.actual_chat, temps, user.id, text)
        print(user.id)
        chat = Query()
        chat.send_query(Query.query_send_message, val)
        
        return 'carre', 200
    except Exception as e:
        print("erreur:", e)
        return 'pas carre la', 500

@app.route('/get-chat-data', methods=['GET'])
def get_chat_data():
    chat_data = user.join_chat(user.actual_chat)
    return jsonify(chat_data)


if __name__ == '__main__':
    app.run(debug=True)