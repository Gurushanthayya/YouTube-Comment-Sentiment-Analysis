from flask import Flask, render_template, request, jsonify
from analyzer import analyze_youtube_video

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No YouTube URL provided"}), 400
        
    url = data['url']
    
    # We will fetch up to 100 comments for analysis
    results = analyze_youtube_video(url, max_comments=100)
    
    if "error" in results:
        return jsonify(results), 500
        
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5005)


