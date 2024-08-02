document.getElementById("messageForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
  
    const message = document.getElementById("message").value;
    const loader = document.querySelector(".loader");  // Select the loader
  
    // Show the loader before fetching data
    loader.style.display = "block";
  
    fetch("/message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.blob();
      })
      .then((data) => {
        const audioPlayer = document.getElementById("audioPlayer");
        const url = URL.createObjectURL(data);
        audioPlayer.src = url;
  
        // Hide the loader when audio starts playing
        audioPlayer.addEventListener("play", function () {
          loader.style.display = "none";
        });
  
        audioPlayer.play();
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
      });
  });
  