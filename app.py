from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatroom123'
socketio = SocketIO(app)

COMMON_USER = 'Brighten'
COMMON_PASS = 'CHNB'
chat_messages = []

themes = [
    {'name': 'Gaming', 'image': 'gaming.jpg'},
    {'name': 'Football', 'image': 'football.jpg'},
    {'name': 'Robots', 'image': 'robots.jpg'},
    {'name': 'Space', 'image': 'space.jpg'},
    {'name': 'Cars', 'image': 'cars.jpg'}
]

def get_current_theme():
    index = int(time.time() / 600) % len(themes)
    return themes[index]

def basic_firewall_check(ip):
    if ip.startswith("192.168.1."):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

        if not basic_firewall_check(ip):
            return "Access Denied by Firewall."

        if username == COMMON_USER and password == COMMON_PASS:
            session['user'] = username
            return redirect(url_for('chat'))
        else:
            return "Wrong credentials. Try again."
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    theme = get_current_theme()
    return render_template('chat.html', theme=theme)

@socketio.on('message')
def handle_message(msg):
    if 'user' in session:
        chat_messages.append(msg)
        send(msg, broadcast=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
