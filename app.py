from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_cors import CORS  # Importa o CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS no Flask
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")  # Permite todas as origens

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Mensagem recebida: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)