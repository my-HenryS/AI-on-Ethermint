var mousePressed = false;
var lastX, lastY;
var ctx;
var myCanvas;
var websocket;
var myConsole;

function InitThis() {
    myConsole = document.getElementById('console');
    myConsole.value = "Waiting for image input ......\n"

    websocket = new WebSocket("ws://127.0.0.1:5001");
    websocket.onmessage = function(evt) {
        result = evt.data;
        if(isResult(result)){
            $("#submit").attr("disabled", false);
            $("#clear").attr("disabled", false);
        }
        myConsole.value = myConsole.value + result;
    };

    myCanvas = document.getElementById('myCanvas');
    ctx = myCanvas.getContext("2d");
    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    $('#myCanvas').mouseup(function (e) {
        mousePressed = false;
    });
        $('#myCanvas').mouseleave(function (e) {
        mousePressed = false;
    });

    ctx.fillStyle="#FFFFFF";
    ctx.fillRect(0,0,ctx.canvas.width, ctx.canvas.height);
}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = $('#selColor').val();
        ctx.lineWidth = $('#selWidth').val();
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}

function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle="#FFFFFF";
    ctx.fillRect(0,0,ctx.canvas.width, ctx.canvas.height);
}

function save() {
    $("#submit").attr("disabled", true);
    $("#clear").attr("disabled", true);
    var image_0 = myCanvas.toDataURL();
    var b64 = image_0.substring( 22 );
    var result;
    websocket.send(b64);
}

function myClose(){
    websocket.close();
}

function isResult(data){
    return data.substring(0,3) == "The"
}


$(function(){
InitThis();
})
