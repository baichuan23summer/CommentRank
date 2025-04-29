// popup.js
document.addEventListener('DOMContentLoaded', async () => {
    const submitButton = document.getElementById('refreshReviews');
    // const reviewInput = document.getElementById('reviewInput');
    const rankedList = document.getElementById('rankedReviews');
    const clearButton = document.getElementById('clearHistory');

    // Load existing reviews from storage
    let reviews = [];
    const storedData = await chrome.storage.local.get('reviews');
    if (storedData.reviews) reviews = storedData.reviews;

    // Submit new review
    submitButton.addEventListener('click', async () => {
        // const reviewText = reviewInput.value.trim();
        // if (!reviewText) {
        //     alert('Please enter a review.');
        //     return;
        // }

        // Add to review history
        // reviews.push(reviewText);
        // await chrome.storage.local.set({ reviews });

        // Send ALL reviews for ranking
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
        const url = new URL(tab.url);
        
        if (!url.hostname.includes('amazon.com')) {
            cookieList.innerHTML = '<li>Not on Amazon page</li>';
            return;
        }
    
        // Get cookies for Amazon domain
        const cookies = await new Promise(resolve => {
            chrome.cookies.getAll({ storeId: '0' }, resolve);
        });
    
        if (cookies.length === 0) {
            console.error("1")
            return;
        }

        // console.log(cookies)

        const cookieHeader = cookies.map(c => {
            return `${c.name}=${c.value}`;
        })

        const response = await fetch('http://localhost:5000/rank', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cookies: cookieHeader })
        });
        console.log(response)
        
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        
        const data = await response.json();
        console.log(data)
        rankedList.innerHTML = '';
        data.forEach((item, index) => {
            const li = document.createElement('li');
            li.textContent = `${index + 1}. (Score: ${item[1].substring(0, 3)}) ${item[2]}`;
            rankedList.appendChild(li);
        });

        // reviewInput.value = ''; // Clear input field
    });

    // Clear history
    clearButton.addEventListener('click', async () => {
        reviews = [];
        await chrome.storage.local.remove('reviews');
        rankedList.innerHTML = '<li>History cleared.</li>';
    });
});
