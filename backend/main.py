import os
import praw
import requests
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# --- FastAPI App Initialization ---
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Clients ---
try:
    # Reddit Client
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    # Gemini Client
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash') 
except Exception as e:
    print(f"Error initializing API clients: {e}")
    reddit = None
    gemini_model = None

# --- Pydantic Models ---
class ContentRequest(BaseModel):
    text: str

# --- Helper Functions ---
def scrape_url_content(url: str):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        # Get text and remove excessive whitespace
        text = ' '.join(soup.stripped_strings)
        return text
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")

def get_keywords_from_gemini(content: str):
    prompt = f"""Analyze the following text and extract the 10 most important keywords or concepts for finding relevant Reddit discussions. Return them as a comma-separated list.

Text:
---
{content[:4000]}
---

Keywords:"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error (keywords): {e}")

def generate_comment_from_gemini(user_content: str, post_title: str, post_body: str):
    prompt = f"""Your goal is to be a 'Smart Engagement Assistant'. You need to create a natural, relevant comment for a Reddit post that should be short readable, engaging try to humorous but dont disrescpect someone sentiments.

Here is the user's content they want to subtly promote:
---
{user_content[:2000]}
---

Here is the Reddit post:
Title: {post_title}
Content: {post_body[:2000]}
---

Generate a comment that adds value to the Reddit discussion and feels authentic. The comment should be relevant to the post first and foremost. If possible, subtly bridge the conversation to the user's content without it feeling like spam. Do not include a direct link.

Comment:"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating comment: {e}" # Return error as string for this specific post

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"Status": "API is running"}

@app.post("/api/analyze-content")
def analyze_content(request: ContentRequest):
    if not reddit or not gemini_model:
        raise HTTPException(status_code=503, detail="API clients not initialized. Check credentials.")

    input_text = request.text.strip()
    
    # 1. Check if input is a URL or direct content
    if input_text.startswith('http://') or input_text.startswith('https://'):
        processed_content = scrape_url_content(input_text)
    else:
        processed_content = input_text

    # 2. Get keywords from Gemini
    keywords_str = get_keywords_from_gemini(processed_content)
    search_query = ' OR '.join([kw.strip() for kw in keywords_str.split(',')])

    # 3. Search Reddit
    try:
        search_results = reddit.subreddit("all").search(search_query, sort='new', limit=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reddit search failed: {e}")

    # 4. Generate comments for each post
    opportunities = []
    for post in search_results:
        if not post.is_self: # Skip posts that are just links
            continue

        comment = generate_comment_from_gemini(
            user_content=processed_content,
            post_title=post.title,
            post_body=post.selftext
        )

        opportunities.append({
            "id": post.id,
            "title": post.title,
            "url": f"https://reddit.com{post.permalink}",
            "subreddit": post.subreddit.display_name,
            "comment_suggestion": comment
        })

    return opportunities
