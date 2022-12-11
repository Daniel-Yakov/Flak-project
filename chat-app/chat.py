from flask import Flask, render_template, request, redirect, url_for
import datetime
import mysql.connector
import socket

massagesDB = mysql.connector.connect(
  host='db',
  user="root",
  password="password",
  database='messagesDB',
  auth_plugin='mysql_native_password'
)

# Act as middlewares between app to mysql
cursor = massagesDB.cursor(buffered=True)
sql = cursor.execute

app = Flask(__name__)

# Render index.html
@app.get("/")
def render_index():
    return render_template("index.html")


# Render index.html
@app.get("/<room>")
def render_index_room(room):
    return render_template("index.html")


# Load chat of specific room
@app.get("/chat/<room>")
def render_chat_room(room):
    sql('create table if not exists ' + room + ' (massageId int NOT NULL AUTO_INCREMENT key, massageContent char(255));')
    return render_template('index.html', host=socket.gethostname())

# Handle the loading of the chat box
@app.get("/api/chat/<room>")
def updateChat(room):
    # Fetch all the chat's massages
    sqlquery = 'select massageContent from %s;' % room
    sql(sqlquery)
    massagesDB.commit()
    
    # Format the output nicly
    chatContent = ""
    for line in cursor.fetchall():
        chatContent += line[0]
    
    return chatContent

# Upadate the chat massages and save then to thier appropriate file
@app.post("/api/chat/<room>")
def sendrequest(room):
    # Format the date as requested
    date = '[' + str(datetime.datetime.now()).split('.')[0] + ']'
    # Prepare the massage before saving to file
    massageToSave = date + ' ' + request.form['username'] + ': ' + request.form['msg'] + '\n'
    
    # Insert the posted massage to the DB
    sqlquery = 'insert into %s (massageContent) values ("%s");' % (room, massageToSave)
    sql(sqlquery)
    massagesDB.commit()

    # redirect to room chat
    return redirect(url_for('render_chat_room', room=room))



if __name__ == '__main__':
    app.run(host='0.0.0.0')