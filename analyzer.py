import re
import itertools
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Comprehensive YouTube Slang, Emoji, & Internet Culture Lexicon
YOUTUBE_SLANG_LEXICON = {
    # High Praise & Positive Slang
    'fire': 2.5,
    'banger': 2.5,
    'goat': 2.8,
    'goated': 2.8,
    'masterpiece': 3.0,
    'peak': 2.2,
    'underrated': 2.0,
    'slay': 2.2,
    'slays': 2.2,
    'slayed': 2.2,
    'goosebumps': 2.2,
    'legend': 2.5,
    'legendary': 2.5,
    'w': 2.0,
    'clutch': 2.2,
    'chill': 1.5,
    'wholesome': 2.5,
    'epic': 2.2,
    'awesome': 2.2,
    'lit': 2.2,
    'dope': 2.0,
    'sick': 1.8,
    'based': 1.8,
    'banging': 2.2,
    'flawless': 2.8,
    'cinema': 2.5,
    'subbed': 1.5,
    'subscribe': 1.0,
    'subscribed': 1.5,
    'banger': 2.5,
    'kudos': 2.0,
    'breathtaking': 2.8,
    'perfection': 2.8,

    # Critical & Negative Slang
    'mid': -1.8,
    'trash': -2.5,
    'cringe': -2.2,
    'cringey': -2.2,
    'cringy': -2.2,
    'flop': -2.2,
    'overrated': -1.8,
    'clickbait': -2.2,
    'scam': -2.8,
    'worst': -2.5,
    'boring': -2.0,
    'horrible': -2.5,
    'terrible': -2.5,
    'rubbish': -2.0,
    'l': -2.0,
    'ratio': -1.5,
    'fake': -2.0,
    'copium': -1.5,
    'disappointed': -2.0,
    'disappointing': -2.2,
    'unsubscribed': -2.2,
    'waste': -2.2,
    'annoying': -2.0,
    'fell off': -2.0,
    'downfall': -2.0,

    # Emojis & Symbols
    '🔥': 2.5,
    '🐐': 2.8,
    '💀': 1.5,    # Laughing hard / hilarious in YouTube context
    '😭': 1.2,    # Laughing crying / emotional
    '❤️': 2.5,
    '💖': 2.5,
    '😍': 2.5,
    '🥰': 2.5,
    '👏': 2.0,
    '💯': 2.2,
    '🙌': 2.0,
    '🗿': 1.5,
    '✨': 1.5,
    '🎉': 2.0,
    '🤩': 2.5,
    '👍': 1.8,
    '🤡': -2.2,
    '💩': -2.5,
    '🤮': -2.5,
    '👎': -2.0,
    '😡': -2.2,
    '🤬': -2.5,
    '📉': -1.8,
}

def init_analyzer():
    analyzer = SentimentIntensityAnalyzer()
    analyzer.lexicon.update(YOUTUBE_SLANG_LEXICON)
    return analyzer

def clean_comment(text):
    """Clean text by removing URLs, timestamps, and excessive whitespace."""
    if not text:
        return ""
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove YouTube timestamps like 01:23 or 4:56
    text = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?\b', '', text)
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_youtube_video(url, max_comments=100):
    downloader = YoutubeCommentDownloader()
    analyzer = init_analyzer()
    
    try:
        # Fetch comments sorted by popularity
        comments_gen = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
        raw_comments = list(itertools.islice(comments_gen, max_comments))
    except Exception as e:
        return {"error": str(e)}

    results = {
        "total_analyzed": 0,
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "average_score": 0.0,
        "comments": []
    }

    total_compound = 0.0

    for comment in raw_comments:
        original_text = comment.get('text', '')
        cleaned = clean_comment(original_text)
        
        if not cleaned:
            continue
            
        scores = analyzer.polarity_scores(cleaned)
        compound = scores['compound']
        total_compound += compound
        
        # Refined sentiment thresholds for YouTube comments
        if compound >= 0.10:
            sentiment = "positive"
            results["positive"] += 1
        elif compound <= -0.10:
            sentiment = "negative"
            results["negative"] += 1
        else:
            sentiment = "neutral"
            results["neutral"] += 1
            
        results["comments"].append({
            "text": original_text,
            "author": comment.get('author', 'Anonymous'),
            "sentiment": sentiment,
            "score": round(compound, 2),
            "votes": comment.get('votes', '0')
        })
        results["total_analyzed"] += 1

    if results["total_analyzed"] > 0:
        results["average_score"] = round(total_compound / results["total_analyzed"], 2)

    return results
