document.getElementById("askButton").addEventListener("click", () => {
  const userDoubt = document.getElementById("doubtInput").value;
  const spinner = document.getElementById("loadingSpinner");
  spinner.style.display = "block"; // show spinner

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { type: "GET_VIDEO_URL" },
      (response) => {
        if (chrome.runtime.lastError) {
          spinner.style.display = "none";
          alert("Error: " + chrome.runtime.lastError.message);
          return;
        }

        const videoUrl = response.url || "URL not found";

        fetch("http://127.0.0.1:5000/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            video_url: videoUrl,
            doubt: userDoubt
          })
        })
          .then((res) => res.json())
          .then((data) => {
            spinner.style.display = "none"; // hide spinner
            if (data.answer) {
              alert("Answer: " + data.answer);
            } else {
              alert("Error: " + data.error);
            }
          })
          .catch((err) => {
            spinner.style.display = "none";
            alert("Request failed: " + err.message);
          });
      }
    );
  });
});

