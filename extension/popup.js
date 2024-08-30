document.addEventListener("DOMContentLoaded", function () {
  const statusElement = document.getElementById("status");

  // Connect to Flask-SocketIO WebSocket server
  const socket = io("http://localhost:5000"); // Ensure Flask is running on this port

  // When a connection is established
  socket.on("connect", () => {
    statusElement.innerText = "Connected to Flask-SocketIO";
    console.log("Connected to WebSocket");
  });
  // Listen for 'voice_command' messages from the backend
  socket.on("voice_command", (data) => {
    statusElement.innerText = `Received voice command: ${data.command}`;
    console.log("Received voice command:", data.command);

    // Change active tab URL based on the command
    // const wikipediaUrl = `https://en.wikipedia.org/wiki/Albert_Einstein#Life_and_career`;
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const currentTab = tabs[0];
      //   console.log(currentTab);
    //   let newUrl = [];

      if (currentTab.url.includes("wikipedia.org/wiki/")) {
        // console.log(newURL);
        fetch("http://localhost:5000/next", {
          method: "POST",

          // Adding body or contents to send
          body: JSON.stringify({
            url: currentTab.url,
          }),

          // Adding headers to the request
          headers: {
            "Content-type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((responseData) => {
            console.log(responseData.url);
            chrome.scripting.executeScript({
              target: { tabId: currentTab.id },
              func: (url) => {
                window.location.href = url;
              },
              args: [responseData.url],
            });
          });
        // Inject script to scroll to the next section
        // console.log(newUrl[0]);
      }
    });
  });

  socket.on("disconnect", () => {
    statusElement.innerText = "Disconnected from Flask-SocketIO";
    console.log("Disconnected from WebSocket");
  });
});
