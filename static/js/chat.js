// Conectar ao servidor WebSocket
//var socket = io();
//var socket = io.connect(window.location.origin);
var socket = io();  // Conecta automaticamente ao servidor de origem


// Evento para capturar a mensagem enviada pelo servidor e exibi-la
socket.on('message', function(msg) {
    var messages = document.getElementById('messages');
    var newMessage = document.createElement('div');
    newMessage.textContent = msg;
    messages.appendChild(newMessage);
});

// Função para enviar a mensagem
document.getElementById('send-btn').onclick = function() {
    var input = document.getElementById('message-input');
    var message = input.value;
    socket.send(message);  // Enviar a mensagem para o servidor
    input.value = '';  // Limpar o campo de entrada
};