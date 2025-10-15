import React, { useState } from 'react';
import './App.css';

function App() {
  const [content, setContent] = useState('');
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const findOpportunities = async () => {
    if (!content) {
      setError('Please enter a URL or paste your content.');
      return;
    }
    setLoading(true);
    setError(null);
    setOpportunities([]);

    try {
      const response = await fetch('/api/analyze-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: content }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setOpportunities(data);

    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>RedditBoss</h1>
        <p>Your Smart Engagement Assistant</p>
      </header>

      <div className="search-container">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Enter your article URL or paste your content here..."
        />
        <button onClick={findOpportunities} disabled={loading}>
          {loading ? 'Finding...' : 'Find Opportunities'}
        </button>
      </div>

      {error && <p className="error">Error: {error}</p>}

      {loading && <p className="loading">Analyzing your content and searching Reddit...</p>}

      <ul className="post-list">
        {opportunities.map((opp) => (
          <li key={opp.id} className="post-item">
            <div className="post-item-header">
              <h3>{opp.title}</h3>
              <span>r/{opp.subreddit}</span>
            </div>
            <div className="post-details">
                <h4>AI-Generated Comment:</h4>
                <div className="comment-suggestion">
                    <span>{opp.comment_suggestion}</span>
                </div>
                <p style={{ marginTop: '15px' }}>
                  <a href={opp.url} target="_blank" rel="noopener noreferrer">View Post on Reddit</a>
                </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
