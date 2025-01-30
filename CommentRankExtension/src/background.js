chrome.commands.onCommand.addListener((command) => {
    if (command === "toggle_sidebar") {
        chrome.scripting.executeScript({
            target: { allFrames: true },
            files: ["content.js"]
        });
    }
});
