from flask import Flask, render_template, request, redirect, url_for
import datetime

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
    # create file if not exist
    try:
        file = open(room, 'x')
    except:
        pass
    return render_template('index.html')

# Handle the loading of the chat box
@app.get("/api/chat/<room>")
def updateChat(room):
    file = open(room)
    return file

# Upadate the chat massages and save then to thier appropriate file
@app.post("/api/chat/<room>")
def sendrequest(room):
    file = open(room, "a+")
    # Format the date as requested
    date = '[' + str(datetime.datetime.now()).split('.')[0] + ']'
    # Prepare the massage before saving to file
    massageToSave = date + ' ' + request.form['username'] + ': ' + request.form['msg'] + '\n'
    # Save the massage to the file
    file.write(massageToSave)
    # redirect to room chat
    return redirect(url_for('render_chat_room', room=room))



if __name__ == '__main__':
    app.run(debug=True)