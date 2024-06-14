const ws = new WebSocket(wsURL);

const editor = document.getElementById('editor');
const lineNumbers = document.getElementById('line-numbers');
let clientUpdate = false;

function updateLineNumbers() {
    const lines = editor.value.split('\n').length;
    let lineNumbersHTML = '';
    for (let i = 1; i <= lines; i++) {
        lineNumbersHTML += '<span>' + i + '</span>';
    }
    lineNumbers.innerHTML = lineNumbersHTML;
}

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (!clientUpdate) {
        editor.value = data.message;
        updateLineNumbers();
    }
    clientUpdate = false;
};

function debounce(func, delay) {
    let timer;
    return function(...args) {
        const context = this;
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(context, args), delay);
    };
}

function sendTextToServer(text) {
    ws.send(JSON.stringify({
        'message': text
    }));
}

editor.addEventListener('input', debounce(function() {
    clientUpdate = true;
    sendTextToServer(editor.value);
    updateLineNumbers();
}, 250));

ws.onclose = function(event) {
    console.error('Chat socket closed unexpectedly');
};

// Initialize line numbers
updateLineNumbers();

// Sync scroll between line numbers and textarea
editor.addEventListener('scroll', function() {
    lineNumbers.scrollTop = editor.scrollTop;
});
