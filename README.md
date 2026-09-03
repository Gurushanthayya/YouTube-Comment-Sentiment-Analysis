# YouTube Comment Sentiment Analysis

A web-based **YouTube Comment Sentiment Analysis** application that uses Natural Language Processing (NLP) to analyze comments from YouTube videos and classify them into **Positive, Neutral, or Negative** sentiments.

The application accepts a YouTube video URL, retrieves up to **100 popular comments**, processes the comment text, and performs sentiment analysis using **VADER Sentiment Analysis**. To make the analysis more suitable for YouTube content, the project includes a custom lexicon containing **YouTube slang, internet expressions, and emojis** such as `fire`, `goat`, `banger`, `trash`, `cringe`, `🔥`, `❤️`, and `👎`.

The project is implemented using **Python and Flask**, with a REST API endpoint that receives the YouTube URL and returns the sentiment analysis results in JSON format.

## Features

* 🔗 Analyze comments using a YouTube video URL
* 💬 Retrieve up to 100 popular YouTube comments
* 🧹 Clean comments by removing URLs, timestamps, and unnecessary whitespace
* 😊 Classify comments as Positive, Neutral, or Negative
* 📊 Calculate an overall average sentiment score
* 🔥 Recognize YouTube-specific slang and expressions
* 😀 Analyze sentiment using emojis and symbols
* 👤 Display comment author information
* 👍 Include comment vote information
* 🌐 Flask-based web application and API


## sentiment classification uses the following thresholds:

* **Positive:** 
* **Neutral:** 
* **Negative:** 

## Technologies Used

* **Python**
* **Flask**
* **VADER Sentiment**
* **YouTube Comment Downloader**
* **Natural Language Processing (NLP)**
* **REST API**

## Project Structure

```text
YouTube-Comment-Sentiment-Analysis/
│
├── app.py
├── analyzer.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── app.js
    └── style.css
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/YouTube-Comment-Sentiment-Analysis.git
cd YouTube-Comment-Sentiment-Analysis
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Flask application:

```bash
python app.py
```

Then open the application in your browser using the local Flask server address.



This version is suitable for a **GitHub repository README** and highlights the NLP, Flask API, YouTube comment extraction, and custom slang/emoji processing that are actually present in your project.
```
