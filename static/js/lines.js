$(document).ready(function(){
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/line")

    // receive new numbers from server
    var numbers_received = [];
    socket.on('new_number', function(msg){
        console.log(msg.number);
        // limit size of the number list to 10
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }
        numbers_received.push(msg.number);
        // render the chart if there's enough data
        if (numbers_received.length >= 10){
            var Config = {
                "type": "line",
                "title": {
                    "text": "Randomly Generated Numbers"
                },
                "series": [{"values": numbers_received}]
            };
            zingchart.render({
                id: "myChart",
                data: Config
            });
        }
    });
});