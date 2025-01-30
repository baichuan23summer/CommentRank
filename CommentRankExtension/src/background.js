chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["src/content.js"],
    });
    console.log("IconClicked");
});

