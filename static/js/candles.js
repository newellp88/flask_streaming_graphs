$(document).ready(function(){
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/candle")

    // receive new numbers from server
    var candles_received = [];
    socket.on('new_candle', function(msg){
        //console.log(msg.candle);
        // limit size of the number list to 10
        if (candles_received.length >= 20){
            candles_received.shift()
        }
        candles_received.push([msg.candle[0], msg.candle[1], msg.candle[2], msg.candle[3]]);
        console.log(candles_received)
        // render the chart if there's enough data
        if (candles_received.length >= 10){
            var Config = {
                "type": "stock",
                "title": {
                    "text": "Randomly Generated Candles"
                },
                "plot": {
                    "aspect": "candlestick"
                },
                "scale-y": {
                    "values": "70:130:2"
                },
                "series": [{"values": candles_received}]
            };
            zingchart.render({
                id: "CandleChart",
                data: Config
            });
        }
    });
});