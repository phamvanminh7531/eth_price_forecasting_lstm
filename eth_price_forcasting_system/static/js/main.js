const ctx = document.getElementById('myChart').getContext('2d');
var graphData = {
    type: 'line',
    data: {
        labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
        datasets: [{
            data: [1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200],
            label: "Current Price",
            borderColor: "#3e95cd",
            fill: false,
            lineTension: 0.2,
        },

        {
            data: [1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200],
            label: "Forcasting Line",
            borderColor: "#3cba9f",
            fill: false,
            lineTension: 0.2,
        },
    
    ]
    },
    options: {
        bezierCurve: true,
        animation : false,
    } 
}
const myChart = new Chart(ctx, graphData);

var socket = new WebSocket('ws://localhost:8000/ws/graph/');

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData)
    
    var newGraphData = graphData.data.datasets[0].data;
    newGraphData.shift();
    newGraphData.push(djangoData.value);
    graphData.data.datasets[0].data = newGraphData;

    var newGraphData2 = graphData.data.datasets[1].data;
    newGraphData2.shift();
    if (djangoData.predict){
        newGraphData2.push(djangoData.predict);
    } else{
        newGraphData2.push(djangoData.predict0);
        newGraphData2.push(djangoData.predict1);
        newGraphData2.push(djangoData.predict2);
        newGraphData2.push(djangoData.predict3);
        newGraphData2.push(djangoData.predict4);
        newGraphData2.push(djangoData.predict5);
    }
    
    graphData.data.datasets[1].data = newGraphData2;
    
    myChart.update();
    document.querySelector('#app').innerText = djangoData.value;
}