document.addEventListener("DOMContentLoaded", () => {
    const routeOutput = document.getElementById("route-output");
    const originSelect = document.getElementById("origin");
    const destinationSelect = document.getElementById("destination");
    const findRouteBtn = document.getElementById("find-route-btn");
  
    const chatOutput = document.getElementById("chat-output");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
  
    // Add message to the chatbox
    function addMessage(sender, message) {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add(sender === "You" ? "user-message" : "bot-message");
      messageDiv.innerHTML = `<div class="bubble">${message}</div>`;
      chatOutput.appendChild(messageDiv);
      chatOutput.scrollTop = chatOutput.scrollHeight;
    }
  
    // Find Route Button Logic
    findRouteBtn.addEventListener("click", async () => {
      const origin = originSelect.value;
      const destination = destinationSelect.value;
  
      if (!origin || !destination) {
        routeOutput.innerHTML = "<p>Please select both origin and destination.</p>";
        return;
      }
  
      try {
        const response = await fetch("http://127.0.0.1:5000/api/route", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ start: origin, end: destination }),
        });
  
        if (!response.ok) {
          throw new Error("Failed to fetch route data.");
        }
  
        const data = await response.json();
        const route = data.route.join(" → ");
        const distance = data.distance;
  
        routeOutput.innerHTML = `
          <p>Route: ${route}</p>
          <p>Distance: ${distance} km</p>
        `;
      } catch (error) {
        routeOutput.innerHTML = `<p>Error: ${error.message}</p>`;
      }
    });
  
    // Chatbot Integration
    sendBtn.addEventListener("click", async () => {
      const userMessage = userInput.value.trim();
      if (!userMessage) {
        addMessage("You", "Please enter a message.");
        return;
      }
  
      addMessage("You", userMessage);
  
      try {
        const response = await fetch("http://127.0.0.1:5000/chatbot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_input: userMessage }),
        });
  
        if (!response.ok) {
          throw new Error("Failed to fetch chatbot response.");
        }
  
        const data = await response.json();
        addMessage("Dei-GO", data.response || "I didn't understand that.");
      } catch (error) {
        addMessage("Dei-GO", `Error: ${error.message}`);
      }
  
      userInput.value = "";
    });
  });