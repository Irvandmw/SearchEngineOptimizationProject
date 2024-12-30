import os
import re
import webbrowser
from difflib import get_close_matches
from flask import Flask, render_template, request

app = Flask(__name__)

# Load Data
data_dir = 'static/data/musicSongs'
songs = {}

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
            songs[filename] = file.read()

# Ambil semua judul lagu
TEXT_FOLDER = "static/data/musicSongs/"
text_files = [
    os.path.join(TEXT_FOLDER, f) for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")
]

titles = []

for file_path in text_files:
    file_name = os.path.basename(file_path)
    title = os.path.splitext(file_name)[0]
    titles.append(title)


# List of common stop words
stop_words = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',
    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
])


def count_single_word(text, word):
    word = word.lower()
    return len(re.findall(r'\b' + re.escape(word) + r'\b', text))

def boolean_retrieval(search_songs, query):
    results = {}
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)
    
    for title, text in search_songs.items():
        matches = True
        for token in tokens:
            if count_single_word(text, token) == 0:
                matches = False
                break
        
        if matches:
            results[title] = matches
            
    return results

def remove_stop_words(text):
    words = text.split()  
    filtered_words = [word for word in words if word not in stop_words]  
    return ' '.join(filtered_words)  

def scan_song(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    cleaned_text = ' '.join(words)
    return cleaned_text

processed_song = {title: scan_song(content) for title, content in songs.items()}

def count_occurrences(text, search_term):
    return text.lower().count(search_term.lower()) 

def search_songs(songs, search_term, limit=20):
    processed_search_term = search_term.lower()
    search_words = processed_search_term.split()

    occurrences = {}

    for title, text in songs.items():
        occurrence_count = 0
        for word in search_words:
            occurrence_count += count_occurrences(text, word)
        occurrences[title] = occurrence_count

    ranked_songs = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)

    return ranked_songs[:limit]


# FLASK
# http://127.0.0.1:5000/
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term'] 
        search_term = search_term.lower()
        ranked_songs_tf = search_songs(processed_song, search_term)
        boolean_results = boolean_retrieval(processed_song, search_term)
        
        return render_template('musicFinder.html',  
                               search_term=search_term,
                               ranked_songs_tf=ranked_songs_tf,
                               boolean_results=boolean_results,
                               )

    return render_template('musicFinder.html')

@app.route('/static/data/musicSongs/<title>')
def show_book(title):
    book_text = songs.get(title)
    if book_text:
        return render_template('readingMode.html', title=title, content=book_text)
    else:
        return "Book not found", 404

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        open_browser()
    app.run(debug=True)