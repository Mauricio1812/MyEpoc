console.log('ws://' + window.location.host + '/ws/pacienteZ')

const socket = new WebSocket('ws://' + window.location.host + '/ws/pacienteZ');

socket.onmessage = function(e){
    console.log('Server: ' + e.data);
};

socket.onopen = function(e){
    socket.send(JSON.stringify({
        'message': 'Hello from client',
    }));
};


// var djangoData = JSON.parse(e.data);
// console.log(djangoData);

// document.querySelector('#app').innerText = djangoData.value;
// };

