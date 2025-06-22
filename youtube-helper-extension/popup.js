document.getElementById("askButton").addEventListener("click", () => {
  const userDoubt = document.getElementById("doubtInput").value;

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { type: "GET_VIDEO_URL" },
      (response) => {
        if (chrome.runtime.lastError) {
          alert("Error: " + chrome.runtime.lastError.message);
          return;
        }

        const videoUrl = response.url || "URL not found";

        // ✅ Send data to Flask backend
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
            if (data.answer) {
              alert("Answer: " + data.answer);
            } else {
              alert("Error: " + data.error);
            }
          })
          .catch((err) => {
            alert("Request failed: " + err.message);
          });
      }
    );
  });
});

