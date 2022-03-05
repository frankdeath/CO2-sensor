window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://10.0.0.110:8765/");

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "data":
        document.querySelector(".CO2").textContent = event.CO2;
        document.title = "CO2: " + event.CO2 + " ppm"
        document.querySelector(".temperature").textContent = event.temperature;
        document.querySelector(".humidity").textContent = event.humidity;
        document.querySelector(".timestamp").textContent = event.timestamp;
        const users = `${event.users} user${event.users == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        break;
      default:
        console.error("unsupported event", event);
    }
  };
});
