import os
import re
import webbrowser
import json
from difflib import get_close_matches
from flask import Flask, render_template, request
from Levenshtein import distance

app = Flask(__name__)

# Load Data
data_dir = 'static/data'
books = {}

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
            books[filename] = file.read()

# Load Data Karakter
CHARACTER_FILE = "static/assets/characters/characters.json"
with open(CHARACTER_FILE, "r", encoding="utf-8") as file:
    characters = json.load(file)

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

def boolean_retrieval(books, query):
    results = {}
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)
    
    for title, text in books.items():
        matches = True
        for token in tokens:
            if count_single_word(text, token) == 0:
                matches = False
                break
        
        if matches:
            results[title] = matches
            
    return results

# Fungsi hapus konjungsi
def remove_stop_words(text):
    words = text.split()  
    filtered_words = [word for word in words if word not in stop_words]  
    return ' '.join(filtered_words)  

def preprocess_text(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    cleaned_text = ' '.join(words)
    return remove_stop_words(cleaned_text)

processed_books = {title: preprocess_text(content) for title, content in books.items()}

def count_occurrences(text, search_term):
    return text.lower().count(search_term.lower())

characters_levenshtein = {
    "Harry Potter", "Hermione Granger", "Ron Weasley", 
    "Albus Dumbledore", "Lord Voldemort", "Severus Snape", 
    "Rubeus Hagrid", "Draco Malfoy", "Sirius Black", 
    "Bellatrix Lestrange", "Neville Longbottom", "Luna Lovegood",
    "Ginny Weasley", "Fred Weasley", "George Weasley",
    "Molly Weasley", "Arthur Weasley", "Minerva McGonagall",
    "Remus Lupin", "Nymphadora Tonks", "Dobby", "Kreacher",
    "Cho Chang", "Cedric Diggory", "Lucius Malfoy", 
    "Narcissa Malfoy", "Fleur Delacour", "Viktor Krum",
    "Peter Pettigrew", "Gilderoy Lockhart"
}

def search_books(books, search_term):
    processed_search_term = remove_stop_words(search_term.lower())
    search_words = processed_search_term.split()

    occurrences = {}
    
    for title, text in books.items():
        occurrence_count = 0
        for word in search_words:
            occurrence_count += count_occurrences(text, word)
        occurrences[title] = occurrence_count

    ranked_books = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    
    return ranked_books 

# FLASK
# http://127.0.0.1:5000/
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term'] 
        search_term = search_term.lower()
        ranked_books_tf = search_books(processed_books, search_term)
        boolean_results = boolean_retrieval(processed_books, search_term)

        closest_matches = get_close_matches(search_term, [char["name"] for char in characters], n=1, cutoff=0.3)
        corrected_term = closest_matches[0] if closest_matches else ''
        print("corrected_term:", corrected_term)
        lower_corrected_term = corrected_term.lower()
        print("lct:",lower_corrected_term)
        lower_search_term = search_term.lower()
        print("lst:", lower_search_term)

        character = None
        if closest_matches:
            match = closest_matches[0]
            character = next(char for char in characters if char["name"] == match)
            print(character)
        
        return render_template('index.html', 
                               closest_matches=closest_matches, 
                               search_term=search_term,
                               lower_search_term=lower_search_term, 
                               lower_corrected_term=lower_corrected_term,
                               ranked_books_tf=ranked_books_tf,
                               boolean_results=boolean_results,
                               match=corrected_term,
                               character=character
                               )

    return render_template('index.html')

@app.route('/static/data/<title>')
def show_book(title):
    book_text = books.get(title)
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