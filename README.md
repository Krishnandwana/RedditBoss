# RedditBoss: Your Smart Engagement Assistant

RedditBoss is a web application designed to help creators, founders, and marketers find and engage with relevant conversations on Reddit. The tool analyzes user-provided content (such as a press release or blog post) and uses AI to discover opportune Reddit posts for engagement, complete with generated comment suggestions.

---

## Features

*   **Content Analysis**: Accepts either a URL to an article or raw text pasted directly into the application.
*   **AI-Powered Keyword Extraction**: Utilizes the Google Gemini API to analyze the source content and extract the most relevant keywords and concepts.
*   **Relevant Post Discovery**: Searches Reddit for recent and relevant posts based on the keywords identified by the AI.
*   **AI-Generated Comment Suggestions**: For each discovered post, the Gemini API generates a unique, context-aware comment designed to be natural and add value to the discussion.
*   **Simple Dashboard**: A clean, straightforward web interface for inputting content and reviewing the generated engagement opportunities.

---

## How It Works

The application follows a simple, powerful workflow:

1.  **Content Input**: The user provides a piece of content, either as a URL or as pasted text.
2.  **Text Processing**: If a URL is provided, the backend scrapes the page to extract its text content. If text is provided, it is used directly.
3.  **Keyword Extraction**: The processed text is sent to the Gemini API, which returns a list of key topics.
4.  **Reddit Search**: The backend uses the Reddit API to search for new posts across all of Reddit that match the key topics.
5.  **Comment Generation**: For each relevant post found, a second call is made to the Gemini API. This call includes both the original source content and the target Reddit post's content, instructing the AI to generate a high-quality comment.
6.  **Display Results**: The frontend receives and displays the list of target posts, each with its tailored comment suggestion.

---

## Tech Stack

*   **Frontend**: React.js
*   **Backend**: Python with the FastAPI framework
*   **APIs**: Google Gemini API, Reddit API
*   **Core Python Libraries**: `praw`, `google-generativeai`, `requests`, `beautifulsoup4`, `python-dotenv`

---

## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

*   Node.js and npm
*   Python 3.8+

### Backend Setup

1.  **Navigate to the server directory**:
    ```bash
    cd D:\Projects\RedditBoss\server
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create and configure the environment file**:
    *   Create a new file named `.env` in the `server` directory.
    *   Add the following variables, replacing the placeholder values with your actual credentials:

    ```
    REDDIT_CLIENT_ID=your_client_id
    REDDIT_CLIENT_SECRET=your_client_secret
    REDDIT_USER_AGENT=A unique user agent string (e.g., RedditBoss v1.0 by u/your_username)
    GEMINI_API_KEY=your_gemini_api_key
    ```

4.  **Get API Keys**:
    *   **Reddit**: Create a 'script' application on your [Reddit Apps page](https://www.reddit.com/prefs/apps).
    *   **Gemini**: Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

5.  **Run the backend server**:
    ```bash
    python -m uvicorn main:app --reload
    ```
    The server will be running at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the client directory**:
    ```bash
    cd D:\Projects\RedditBoss\client
    ```

2.  **Install Node.js dependencies**:
    ```bash
    npm install
    ```

3.  **Run the frontend application**:
    ```bash
    npm start
    ```
    This will open the application in your default web browser at `http://localhost:3000`.

---

## Usage

1.  Ensure both the backend and frontend servers are running.
2.  Open your web browser to `http://localhost:3000`.
3.  Paste your article's URL or its full text into the text area.
4.  Click the "Find Opportunities" button.
5.  Review the list of suggested Reddit posts and the AI-generated comments for each one.
