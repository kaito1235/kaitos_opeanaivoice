document.getElementById("messageForm").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission

  const message = document.getElementById("message").value;

  fetch("/message", {
    method: "POST", // Make sure the method is POST
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: message }), // Send the message as JSON
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((data) => {
      const audioPlayer = document.getElementById("audioPlayer");
      audioPlayer.src = URL.createObjectURL(data);
      audioPlayer.play();
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
});
