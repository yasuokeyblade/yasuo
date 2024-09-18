import pika
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Função para enviar mensagem para o RabbitMQ
def send_to_rabbitmq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))
    channel = connection.channel()
    channel.queue_declare(queue='chatQueue')
    channel.basic_publish(exchange='', routing_key='chatQueue', body=message)
    connection.close()

# Função para consumir mensagem do RabbitMQ
def consume_from_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))
    channel = connection.channel()
    channel.queue_declare(queue='chatQueue')

    def callback(ch, method, properties, body):
        # Emitir a mensagem para todos os clientes conectados via WebSocket
        socketio.emit('message', body.decode())  # Removi o argumento 'broadcast=True'

    channel.basic_consume(queue='chatQueue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Mensagem recebida: ' + msg)
    # Envia a mensagem para o RabbitMQ
    send_to_rabbitmq(msg)

if __name__ == '__main__':
    # Executa o consumidor RabbitMQ em uma thread separada
    socketio.start_background_task(target=consume_from_rabbitmq)
    socketio.run(app, host='0.0.0.0', port=5000)
