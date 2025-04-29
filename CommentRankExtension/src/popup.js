// popup.js
document.addEventListener('DOMContentLoaded', async () => {
    const submitButton = document.getElementById('refreshReviews');
    const rankedList = document.getElementById('rankedReviews');
    const clearButton = document.getElementById('clearHistory');
    
    submitButton.addEventListener('click', async () =>{
        // Show loading state
        rankedList.innerHTML = '<li>Loading product reviews...</li>';

        try {
            // Get current tab URL
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            const url = new URL(tab.url);
            
            // Extract ASIN from Amazon URL
            const asin = extractASIN(url.pathname);
            if (!asin) {
                rankedList.innerHTML = '<li>'+asin+'</li>';
                return;
            }
            
            // Extract cookies
            const cookies = await new Promise(resolve => {
                chrome.cookies.getAll({ storeId: '0' }, resolve);
            });

            if (cookies.length === 0) {
                console.error("1")
                return;
            }
            console.log(asin, "\n", cookies)

            const cookieHeader = cookies.map(c => {

                return `${c.name}=${c.value}`;

            })

            // Send ASIN to API
            const response = await fetch('http://localhost:5000/get-reviews', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ asin, cookieHeader })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            renderResults(data);

        } catch (error) {
            console.error('Error:', error);
            rankedList.innerHTML = '<li>Error fetching reviews. Please try again.</li>';
        }
    });

    clearButton.addEventListener('click', async () => {
        rankedList.innerHTML = '<li>History cleared.</li>';
    });
});

function extractASIN(path) {
    // Match ASIN in common Amazon URL patterns
    const asinRegex = /\/(?:dp|gp\/product)\/([A-Z0-9]{10})/;
    const match = path.match(asinRegex);
    return match ? match[1] : null;
}

function renderResults(data) {
    const rankedList = document.getElementById('rankedReviews');
    rankedList.innerHTML = ''; // Clear previous results

    // Handle null/undefined data or empty response
    if (!data?.test_reviews?.length) {
        const message = !data ? 'Error fetching data' : 
                       data.test_reviews ? 'No reviews found' : 'Invalid data format';
        rankedList.innerHTML = `<li class="error">${message}</li>`;
        return;
    }

    // Create document fragment for batch DOM insertion
    const fragment = document.createDocumentFragment();
    
    // Using map + append instead of forEach for better performance
    rankedList.append(...data.test_reviews.map((item, index) => {
        const li = document.createElement('li');
        
        // Safely handle potential missing values
        const score = item.score?.toFixed?.(2) ?? 'N/A';
        const reviewText = item.review || 'No review text available';

        li.innerHTML = `
            <div class="review-item">
                <span class="rank">${index + 1}.</span>
                <span class="score">Score: ${score}</span>
                <p class="review-text">${reviewText}</p>
            </div>
        `;
        return li;
    }));

    // Optional: Add data attributes for debugging
    rankedList.dataset.lastUpdated = new Date().toISOString();
}