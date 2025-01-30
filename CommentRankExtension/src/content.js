(async function () {
    console.log("CommentRank Sidebar Injected");

    if (document.getElementById("commentRank-sidebar")) return;

    // Create the sidebar container
    let sidebar = document.createElement("div");
    sidebar.id = "commentRank-sidebar";
    sidebar.innerHTML = `
        <iframe src="${chrome.runtime.getURL("pages/sidebar.html")}" id="commentRank-frame"></iframe>
        <button id="commentRank-close">✖</button>
    `;
    
    document.body.appendChild(sidebar);

    // Close button functionality
    document.getElementById("commentRank-close").addEventListener("click", () => {
        sidebar.remove();
    });
})();
