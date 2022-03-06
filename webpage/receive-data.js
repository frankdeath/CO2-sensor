var maxPoints = 60;
var counter = 0;
var indices = new Array;
var values = new Array;

window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://10.0.0.110:8765/");

  /*PLOT = document.getElementById('plot'); 
  Plotly.newPlot( PLOT, [{ 
  x: indices,
  y: values }], {
  margin: { t: 0 } } );*/

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "data":
	counter = counter + 1;
	sz = indices.push(counter);
        if (sz > maxPoints)
	{
	  indices.shift();
	}
        sz = values.push(parseFloat(event.CO2));
        if (sz > maxPoints)
	{
	  values.shift();
	}
        document.querySelector(".CO2").textContent = event.CO2;
        document.title = "CO2: " + event.CO2 + " ppm"
        document.querySelector(".temperature").textContent = event.temperature;
        document.querySelector(".humidity").textContent = event.humidity;
        document.querySelector(".timestamp").textContent = event.timestamp;
        const users = `${event.users} user${event.users == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        /* Update the plot */
        /*Plotly.react( PLOT, [{
        x: indices,
        y: values }]);*/
        
        break;
      default:
        console.error("unsupported event", event);
    }
  };
});
