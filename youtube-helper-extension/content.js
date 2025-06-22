// content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_VIDEO_URL") {
    const videoUrl = window.location.href;
    sendResponse({ url: videoUrl });
  }
});
