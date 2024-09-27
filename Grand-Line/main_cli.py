import mysql.connector
from dotenv import load_dotenv
import os
import datetime
from hashlib import sha256
import requests
import time
from flask import Flask,render_template,redirect
application = Flask(__name__)

env = ".env"
load_dotenv(env)


config = {
    'host': os.getenv("DATABASE_HOST"),
    'user': os.getenv("DATABASE_USERNAME"),
    'passwd': os.getenv("DATABASE_PASSWORD"),
    'db': os.getenv("DATABASE"),

}

def clearConsole():
    command = "clear"
    if os.name in ("nt", "dos"):  
        command = "cls"
    os.system(command)
class Query:
    query_message = """INSERT INTO `grandlinedb`.`chat` (ID, time,  expediteur, message) VALUES (0, %s, %s, %s)"""
    query_signup="""INSERT INTO `grandlinedb`.`user` (name, password, IP) VALUES (%s, %s, %s)"""
    query_login = """SELECT * FROM user WHERE name = %s AND passwd = %s"""
    query_accountslist="SELECT name FROM user"
    
    def send_query(query, val):
        conection = mysql.connector.connect(**config)
        cursor = conection.cursor()
        cursor.execute(query, val)
        conection.commit()
    query_login = """SELECT * FROM `grandlinedb`.`user` WHERE name = %s AND password = %s"""
    query_friend_list = """SELECT u.name, f.ID
                        FROM friends f
                        JOIN user u ON f.mem_2 = u.id
                        WHERE f.mem_1 = %s AND f.valid = 1
                        UNION
                        SELECT u.name, f.ID
                        FROM friends f
                        JOIN user u ON f.mem_1 = u.id
                        WHERE f.mem_2 = %s AND f.valid = 1;"""
    query_friend_add ="""INSERT INTO `grandlinedb`.`friends` (mem_1, mem_2)
                        SELECT %s, id FROM `grandlinedb`.`user` WHERE name = %s;"""
    query_friend_request = """SELECT user.name, friends.ID
                        FROM friends
                        JOIN user ON friends.mem_2 = user.id and friends.valid = 0
                        WHERE friends.mem_1 = %s
                        UNION SELECT user.name, friends.ID
                        FROM friends
                        JOIN user ON friends.mem_1 = user.id and friends.valid = 0
                        WHERE friends.mem_2 = %s;"""
    query_accept_friend_requests ="""UPDATE `grandlinedb`.`friends` SET `valid`=1 WHERE  `ID`=%s;"""
    query_display_chat = """SELECT ID, time, message, expediteur FROM `grandlinedb`.`chat` WHERE ID = %s ORDER BY time ASC;"""
    query_send_message = """INSERT INTO `grandlinedb`.`chat` (ID, time,  expediteur, message) VALUES (%s, %s, %s, %s);"""
    query_island_size = """SELECT COUNT(mess_id) FROM chat WHERE ID = %s;"""

    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor(buffered=True)
        
    def send_query(self, query, val):
        
        self.cursor.execute(query, val)
        self.conn.commit()

class User:
    def __init__(self,passwd=None ,id=None,ip=None, name=None):#J'ai mis passwd à none car initialisé dans signup
        self.id=id
        self.name = name        
        self.passwd = passwd    
        self.ip = ip
        self.demande= {}
        self.chat = {}
        self.auth = False
        self.actual_chat = 0
            
    def password(self):
        special_characters = "!@#$%^&*()-+?_=,<>/"
        numeros="1234567890"
        maj="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        password_attempt=str(input("Account Password (au moins un car spécial, un numero et une majuscule ) ?: "))
        if any(car in special_characters for car in password_attempt) and any(num in numeros for num in password_attempt) and any(upper in maj for upper in password_attempt):
            self.passwd=password_attempt
        else :
            print(False)
            self.password()

    def signup(self):

        self.name=str(input("Username ?: "))
        self.password()
        self.passwd=sha256(self.passwd.encode('utf-8')).hexdigest()
        self.ip=requests.get('https://api.ipify.org').text
        print(self.passwd)
        result= Query()
        result.send_query(Query.query_signup,(self.name,self.passwd,self.ip))
        self.auth = True
    
    def login(self):
        self.name = str(input("username : "))
        self.passwd = str(input("mdp : "))
        result = Query()
        result.send_query(Query.query_login, (self.name, sha256(self.passwd.encode('utf-8')).hexdigest())) 
        col = result.cursor.fetchall()
        if col:  
            self.auth = True
            self.id = col[0][0]
            self.ip = col[0][3]
        else:
            print("Mauvais identifiant")
        
    def friend_list(self):
        amis = Query()  
        val = (self.id,self.id)
        amis.send_query(Query.query_friend_list, val)
        rows = amis.cursor.fetchall() 
        
        if not rows:  
            print("Vous n'avez pas d'amis :")
        else:
            print("Voici vos Discussion avec vos amis : ")  
            for row in rows :
                if isinstance(row, tuple):                                      
                    self.chat[row[0]] = int(row[1])
                    print(f'                {row[0]}')
        
        print("Voici vos demandes d'amis en cours :")
        amis.send_query(Query.query_friend_request, (self.id, self.id ))
        rows = amis.cursor.fetchall()
        for row in rows:            
            if isinstance(row, tuple): 
                self.demande[row[0]] = int(row[1])
                print(f'                {row[0]} veut devenir votre ami')
    
    def add_friends(self):
        amis = Query()
        val = str(input("Quelle est le nom de votre amis ? : "))
        amis.send_query(Query.query_friend_add, (self.id,val ))
            
    def accept_friend_requests(self):
        
        try:
            amis= Query()
            friend = str(input("Qui veut tu accepter ?"))
            val = self.demande[friend]
            amis.send_query(Query.query_accept_friend_requests, (val, ))
            print("Vous avez accepté ", friend ," dans vos amis !")
        except:
            print("petit probleme")
            
    def join_chat(self):
        chat = str(input('Quelle discussion voulez-vous rejoindre ? : '))
        self.actual_chat = self.chat[chat]
        display = Query()
        display.send_query(Query.query_display_chat, (self.actual_chat,))
        result = display.cursor.fetchall()
        init = False

        while True:
            try:
                display.send_query(Query.query_display_chat, (self.actual_chat,))
                cur_messages = display.cursor.fetchall()

                if cur_messages != result or not init:
                    for mess in cur_messages:
                        if mess[3] == self.id:
                            print(self.name, " à ", mess[1], " : \n", mess[2])
                        else:
                            print(chat, " à ", mess[1], " : \n", mess[2])
                    result = cur_messages
                    init = True
                else:
                    self.send_chat()
                        
                time.sleep(1)

            except Exception as e:
                print(e)
        
    def send_chat(self):
        try:   
            text = str(input("Entrez votre message  ?: "))
                
            temps = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val = (self.actual_chat,temps, self.id, text)
            chat = Query()
            chat.send_query(Query.query_send_message, val)
        except Exception as err:
            print(err)
            print("petit probleme")

    matrice=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def spawn_island(self):
        try:
            amis = Query()  
            val = (self.id,self.id)  
            amis.send_query(Query.query_friend_list, val)  
            rows = amis.cursor.fetchall()
            nbr_mess=Query()
            print(rows)
            for row in rows:
                a=(row[1],)
                nbr_mess.send_query(Query.query_island_size,a)
                b=nbr_mess.cursor.fetchall()
                print(b[0][0],a[0])
        except Exception as e:
            (print(e))

user=User()
user.login()
user.friend_list()
user.join_chat()
user.send_chat()