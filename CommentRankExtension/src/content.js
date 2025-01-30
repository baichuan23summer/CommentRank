(async function () {
    console.log("CommentRank Sidebar Toggle Triggered");

    // Check if sidebar already exists
    let existingSidebar = document.getElementById("commentRank-sidebar");
    if (existingSidebar) {
        existingSidebar.remove(); // Close sidebar if it exists
        return;
    }

    // Create sidebar container
    let sidebar = document.createElement("div");
    sidebar.id = "commentRank-sidebar";

    // Fetch the sidebar.html content and insert it inside the div
    fetch(chrome.runtime.getURL("sidebar.html"))
        .then(response => response.text())
        .then(html => {
            sidebar.innerHTML = html;
            document.body.appendChild(sidebar);
        })
        .then(() => {
            console.log("fetch successful");
        })
        .catch(err => console.error("Error loading sidebar:", err));

    sidebar.classList.add("commentRank-sidebar");

})();
