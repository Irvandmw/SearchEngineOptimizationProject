from flask import Flask, render_template, request
import os
import re
import webbrowser

app = Flask(__name__)

# Load Data
data_dir = 'data'
books = {}

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
            books[filename] = file.read()

# Define a set of stop words
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
    'will', 'just', 'don', 'should', 'now'
])

# Preprocess text to handle punctuation and possessives
def preprocess_text(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# Preprocess each book
processed_books = {title: preprocess_text(content) for title, content in books.items()}

# Function to count occurrences of a single word in text
def count_single_word(text, word):
    word = word.lower()
    return len(re.findall(r'\b' + re.escape(word) + r'\b', text))

# Function to count total occurrences of all words in the search term
def count_occurrences(text, search_term):
    search_words = search_term.lower().split()
    total_count = sum(count_single_word(text, word) for word in search_words)
    return total_count

# Function to search and rank books based on total occurrences of all words in the search term
def search_books_tf(books, search_term):
    occurrences = {title: count_occurrences(text, search_term) for title, text in books.items()}
    ranked_books = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    return ranked_books

# Boolean retrieval function
def boolean_retrieval(books, query):
    results = {}
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)
    
    for title, text in books.items():
        matches = True
        for token in tokens:
            if token.startswith("not "):
                search_term = token[4:]
                if count_single_word(text, search_term) > 0:
                    matches = False
                    break
            else:
                if count_single_word(text, token) == 0:
                    matches = False
                    break
        
        if matches:
            results[title] = matches
            
    if not results:
        return f'The search term "{query}" does not match any books.'
    
    return results

# FLASK
# http://127.0.0.1:5000/
# Go to the above URL to run the search engine in your browser
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        ranked_books_tf = search_books_tf(processed_books, search_term)
        boolean_results = boolean_retrieval(processed_books, search_term)
        
        if isinstance(boolean_results, str):
            return render_template('index.html', 
                                   search_term=search_term, 
                                   ranked_books_tf=ranked_books_tf,
                                   boolean_message=boolean_results)
        
        return render_template('index.html', 
                               search_term=search_term, 
                               ranked_books_tf=ranked_books_tf,
                               boolean_results=boolean_results)
    return render_template('index.html')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    open_browser()
    app.run(debug=True)