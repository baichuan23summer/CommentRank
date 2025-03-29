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
    // Function to fetch Amazon product comments with detailed metrics
    async function fetchAmazonComments() {
        const comments = [];
        try {
            // Get all review elements on the page
            const reviewElements = document.querySelectorAll('[data-hook="review"]');
            
            reviewElements.forEach(review => {
                // Basic review information
                const rating = review.querySelector('[data-hook="review-star-rating"]')?.textContent;
                const title = review.querySelector('[data-hook="review-title"]')?.textContent;
                const body = review.querySelector('[data-hook="review-body"]')?.textContent;
                const date = review.querySelector('[data-hook="review-date"]')?.textContent;
                const authorName = review.querySelector('.a-profile-name')?.textContent;
                
                // Review metrics
                const helpfulVotes = review.querySelector('[data-hook="helpful-vote-statement"]')?.textContent;
                const verifiedPurchase = review.querySelector('[data-hook="avp-badge"]') !== null;
                const images = Array.from(review.querySelectorAll('[data-hook="review-image"]')).map(img => img.src);
                const videos = Array.from(review.querySelectorAll('[data-hook="review-video"]')).map(video => video.src);
                
                // Parse helpful votes count
                let helpfulCount = 0;
                if (helpfulVotes) {
                    const match = helpfulVotes.match(/\d+/);
                    helpfulCount = match ? parseInt(match[0]) : 0;
                }

                comments.push({
                    rating: rating?.trim(),
                    title: title?.trim(),
                    body: body?.trim(),
                    date: date?.trim(),
                    author: authorName?.trim(),
                    helpfulVotes: helpfulCount,
                    isVerifiedPurchase: verifiedPurchase,
                    mediaContent: {
                        images: images,
                        videos: videos
                    },
                    reviewId: review.getAttribute('id'),
                    profileLink: review.querySelector('.a-profile')?.href
                });
            });
            
            return comments;
        } catch (error) {
            console.error('Error fetching Amazon comments:', error);
            return [];
        }
    }

})();
