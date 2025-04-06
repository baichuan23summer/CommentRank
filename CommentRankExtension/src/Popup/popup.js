// popup.js
document.addEventListener('DOMContentLoaded', async () => {
    const submitButton = document.getElementById('submitReview');
    const reviewInput = document.getElementById('reviewInput');
    const rankedList = document.getElementById('rankedReviews');
    const clearButton = document.getElementById('clearHistory');

    // Load existing reviews from storage
    let reviews = [];
    const storedData = await chrome.storage.local.get('reviews');
    if (storedData.reviews) reviews = storedData.reviews;

    // Submit new review
    submitButton.addEventListener('click', async () => {
        const reviewText = reviewInput.value.trim();
        if (!reviewText) {
            alert('Please enter a review.');
            return;
        }

        // Add to review history
        reviews.push(reviewText);
        await chrome.storage.local.set({ reviews });

        // Send ALL reviews for ranking
        try {
            const response = await fetch('http://localhost:5000/rank', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ reviews })
            });
            
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            
            const data = await response.json();
            rankedList.innerHTML = '';
            data.forEach((item, index) => {
                const li = document.createElement('li');
                li.textContent = `${index + 1}. (Score: ${item.score.toFixed(2)}) ${item.review}`;
                rankedList.appendChild(li);
            });

            reviewInput.value = ''; // Clear input field
        } catch (error) {
            console.error('Error:', error);
            rankedList.innerHTML = '<li>Failed to rank reviews. Check API.</li>';
        }
    });

    // Clear history
    clearButton.addEventListener('click', async () => {
        reviews = [];
        await chrome.storage.local.remove('reviews');
        rankedList.innerHTML = '<li>History cleared.</li>';
    });
});