let sentimentChart = null;

document.getElementById('analyze-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const urlInput = document.getElementById('url-input').value;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('span');
    const spinner = document.getElementById('spinner');
    const errorMsg = document.getElementById('error-message');
    const resultsSection = document.getElementById('results-section');
    
    // UI Loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    spinner.style.display = 'block';
    errorMsg.style.display = 'none';
    resultsSection.style.display = 'none';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: urlInput })
        });
        
        const data = await response.json();
        
        if (!response.ok || data.error) {
            throw new Error(data.error || 'Failed to analyze video');
        }
        
        renderResults(data);
        resultsSection.style.display = 'flex';
        
    } catch (err) {
        errorMsg.textContent = err.message;
        errorMsg.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        btnText.textContent = 'Analyze';
        spinner.style.display = 'none';
    }
});

function renderResults(data) {
    // 1. Update stats
    const total = data.total_analyzed;
    document.getElementById('total-count').textContent = total;
    
    if (total > 0) {
        document.getElementById('stat-pos').textContent = Math.round((data.positive / total) * 100) + '%';
        document.getElementById('stat-neu').textContent = Math.round((data.neutral / total) * 100) + '%';
        document.getElementById('stat-neg').textContent = Math.round((data.negative / total) * 100) + '%';
    } else {
        document.getElementById('stat-pos').textContent = '0%';
        document.getElementById('stat-neu').textContent = '0%';
        document.getElementById('stat-neg').textContent = '0%';
    }

    // 2. Render Chart
    const ctx = document.getElementById('sentiment-chart').getContext('2d');
    
    if (sentimentChart) {
        sentimentChart.destroy();
    }
    
    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [data.positive, data.neutral, data.negative],
                backgroundColor: [
                    '#10b981', // pos
                    '#64748b', // neu
                    '#ef4444'  // neg
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#f8fafc' }
                }
            },
            cutout: '70%'
        }
    });

    // 3. Render Comments
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = ''; // clear old
    
    data.comments.forEach(comment => {
        const card = document.createElement('div');
        card.className = `comment-card ${comment.sentiment}`;
        
        card.innerHTML = `
            <div class="comment-header">
                <span class="comment-author">@${comment.author} &bull; Score: ${comment.score}</span>
                <span class="sentiment-badge ${comment.sentiment}">${comment.sentiment}</span>
            </div>
            <p class="comment-text">${escapeHtml(comment.text)}</p>
        `;
        
        commentsList.appendChild(card);
    });
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
