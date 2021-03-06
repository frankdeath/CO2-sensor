var maxPoints = 60;
var counter = 0;
var timestamps = new Array;
var values = new Array;

function makeChart(data) {
  console.time('chart');

  let interval = 2000;

  const opts = {
    title: "CO2 vs Time",
    width: 800,
    height: 300,
    cursor: {
      drag: {
        setScale: false,
      }
    },
    select: {
      show: false,
    },
    series: [
      {},
      {
        label: "CO2",
	scale: "ppm",
	value: (u, v) => v == null ? "-" : v.toFixed(1) + "ppm",
	stroke: "red",
      },
    ],
    axes: [
      {},
      {
        scale: "ppm",
        values: (u, vals, space) => vals.map(v => +v.toFixed(1) + "ppm"),
      },
    ]
  };
  
  let start = 0;
  let co2plot = new uPlot(opts, data, document.getElementById('plot'));
  
  return co2plot;
}

window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://10.0.0.110:8765/");

  chart = null;

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "history":
        for (let i = 0; i < event.timestamps.length; i++)
        {
          timestamps.push(event.timestamps[i]);
	  values.push(parseFloat(event.values[i]));
	}
        chart = makeChart([timestamps, values]);
        // fall through to the data case so that the web page updates immediately after loading
      case "data":
	counter = counter + 1;
	sz = timestamps.push(event.timestamp);
        if (sz > maxPoints)
	{
	  timestamps.shift();
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
        document.querySelector(".datetime").textContent = event.datetime;
        const users = `${event.users} user${event.users == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        document.querySelector(".self_calibration").textContent = event.self_calibration;
        document.querySelector(".calibration_reference").textContent = event.calibration_reference;
        /* Manually update the plot */
        chart.setData([timestamps, values]);
        break;
      default:
        console.error("unsupported event", event);
    }
  };
});
