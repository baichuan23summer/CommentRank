document.addEventListener("DOMContentLoaded", async function () {
    console.log("Sidebar loaded");

    // Simulating fetching reviews
    let reviews = [
        { text: "Great product!", score: 9.5 },
        { text: "It's okay.", score: 6.0 },
        { text: "Not worth it.", score: 3.2 }
    ];

    let reviewsList = document.getElementById("reviews-list");
    reviews.forEach(review => {
        let li = document.createElement("li");
        li.textContent = `${review.text} - Score: ${review.score}`;
        reviewsList.appendChild(li);
    });
});
