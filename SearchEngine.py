import Levenshtein
import os
import re
import webbrowser
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

# Process text to remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    # Filter konjungsi
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# Fungsi ngitung kata yang sama per-kata saja
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
            
    if not results:
        return f'The search term "{query}" does not match any books.'
    
    return results

# Fungsi hapus konjungsi
def remove_stop_words(text):
    words = text.split()  # Split text into words
    filtered_words = [word for word in words if word not in stop_words]  # Filter out stop words
    return ' '.join(filtered_words)  # Join words back into a string

# Updated preprocess function to include stop word removal
def preprocess_text(text):
    text = text.lower()
    # Remove punctuation by keeping only word characters and spaces between them
    words = re.findall(r'\b\w+\b', text)
    # Join words into a single string separated by spaces
    cleaned_text = ' '.join(words)
    # Remove stop words
    return remove_stop_words(cleaned_text)

processed_books = {title: preprocess_text(content) for title, content in books.items()}

# Fungsi untuk menghitung total kata yang sama
def count_occurrences(text, search_term):
    return text.lower().count(search_term.lower())

characters = {
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


# def correct_search_term(search_term,characters):
#     closest_match = None
#     min_distance = float('inf')

#     # Iterasi setiap nama karakter
#     for character in characters:
#         # Hitung jarak Levenshtein
#         character = character.lower()
#         dist = Levenshtein.distance(search_term.lower(), character.lower())
#         if dist < min_distance: 
#             min_distance = dist
#             closest_match = character
#             print(character)
            
#     return closest_match
    
#     # words = search_term.lower().split()
#     # corrected_words = []

#     # for word in words:
#     #     corrected_word = word 
#     #     for correct_term, misspellings in characters.items():
#     #         if word in misspellings:
#     #             corrected_word = correct_term  
#     #             break
#     #     corrected_words.append(corrected_word)
    
#     # # Join digunakan untuk menyatukan lagi kata
#     # return ' '.join(corrected_words)

def correct_search_term(search_term, characters):
    closest_match = None
    min_distance = float('inf')
    

    # Check for exact matches (case-insensitive)
    for character in characters:
        character = character.lower()
        if search_term.lower() == character.lower():
            return character  # Exact match found

    # Check for partial matches
    for character in characters:
        character = character.lower()
        if search_term.lower() in character.lower():
            return character  # Partial match found

    # Fallback to Levenshtein distance
    for character in characters:
        character = character.lower()
        dist = Levenshtein.distance(search_term.lower(), character.lower())
        if dist < min_distance: 
            min_distance = dist
            closest_match = character

    return closest_match


def search_books(books, search_term):
    processed_search_term = remove_stop_words(search_term.lower())
    search_words = processed_search_term.split()
    corrected_search_term = [correct_search_term(term, characters) for term in search_words]

    occurrences = {}
    
    for title, text in books.items():
        occurrence_count = 0
        for word in corrected_search_term:
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
        print(search_term)
        ranked_books_tf = search_books(processed_books, search_term)
        boolean_results = boolean_retrieval(processed_books, search_term)
        corrected_search_term = correct_search_term(search_term, characters)
        print("Hello world")
        if corrected_search_term!=search_term:
            if isinstance(boolean_results, str):
                return render_template('index.html', 
                                    search_term=search_term, 
                                    ranked_books_tf=ranked_books_tf,
                                    boolean_message=boolean_results,
                                    corrected_search_term=corrected_search_term)
            
            return render_template('index.html', 
                                search_term=search_term, 
                                ranked_books_tf=ranked_books_tf,
                                boolean_results=boolean_results,
                                corrected_search_term=corrected_search_term)
        else:
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
    from flask import Flask, render_template, request
from difflib import get_close_matches
import os
import re
import webbrowser
import json


app = Flask(__name__)

# Load Data Buku
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

# Process text to remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    # Filter konjungsi
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# Fungsi ngitung kata yang sama per-kata saja
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
            
    if not results:
        return f'The search term "{query}" does not match any books.'
    
    return results

# Fungsi hapus konjungsi
def remove_stop_words(text):
    words = text.split()  # Split text into words
    filtered_words = [word for word in words if word not in stop_words]  # Filter out stop words
    return ' '.join(filtered_words)  # Join words back into a string

# Updated preprocess function to include stop word removal
def preprocess_text(text):
    text = text.lower()
    # Remove punctuation by keeping only word characters and spaces between them
    words = re.findall(r'\b\w+\b', text)
    # Join words into a single string separated by spaces
    cleaned_text = ' '.join(words)
    # Remove stop words
    return remove_stop_words(cleaned_text)

processed_books = {title: preprocess_text(content) for title, content in books.items()}

# Fungsi untuk menghitung total kata yang sama
def count_occurrences(text, search_term):
    return text.lower().count(search_term.lower())

character_corrections = {
    "harry": ["hary", "hari", "haru"],
    "potter": ["poter", "pottr", "poterr"],
    "hermione": ["hermione", "hermion"],
    "ron": ["ronn", "ronny"],
    "dumbledore": ["dumbldore", "dumbeldore"],
    "snape": ["sneap", "snap"],
    "voldemort": ["voldemort", "voldemortt", "voldermort"],
    "draco": ["drako", "draco"],
    "hagrid": ["haggrid", "hagridd"],
    "ginny": ["ginny", "ginni"],
    "luna": ["luna", "loona"],
}

def correct_search_term(search_term):
    words = search_term.lower().split()
    corrected_words = []

    for word in words:
        corrected_word = word 
        for correct_term, misspellings in character_corrections.items():
            if word in misspellings:
                corrected_word = correct_term  
                break
        corrected_words.append(corrected_word)
    
    # Join digunakan untuk menyatukan lagi kata
    return ' '.join(corrected_words)

def search_books(books, search_term):
    processed_search_term = remove_stop_words(search_term.lower())
    search_words = processed_search_term.split()
    corrected_search_term = [correct_search_term(term) for term in search_words]

    occurrences = {}
    
    for title, text in books.items():
        occurrence_count = 0
        for word in corrected_search_term:
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
        ranked_books_tf = search_books(processed_books, search_term)
        boolean_results = boolean_retrieval(processed_books, search_term)
        corrected_search_term = correct_search_term(search_term)
        names = [char["name"] for char in characters]
        closest_matches = get_close_matches(search_term, names, n=1, cutoff=0.3)
        
        if corrected_search_term!=search_term:
            if isinstance(boolean_results, str):
                if closest_matches:
                    match = closest_matches[0]
                    character = next(char for char in characters if char["name"] == match)
                    return render_template('index.html', 
                                        search_term=search_term, 
                                        ranked_books_tf=ranked_books_tf,
                                        boolean_message=boolean_results,
                                        corrected_search_term=corrected_search_term,
                                        character=character)
            if closest_matches:
                match = closest_matches[0]
                character = next(char for char in characters if char["name"] == match)
                return render_template('index.html', 
                                    search_term=search_term, 
                                    ranked_books_tf=ranked_books_tf,
                                    boolean_results=boolean_results,
                                    corrected_search_term=corrected_search_term,
                                    character=character)
        else:
            if isinstance(boolean_results, str):
                if closest_matches:
                    match = closest_matches[0]
                    character = next(char for char in characters if char["name"] == match)
                    return render_template('index.html',
                                        search_term=search_term, 
                                        ranked_books_tf=ranked_books_tf,
                                        boolean_message=boolean_results,
                                        character=character)
            if closest_matches:
                match = closest_matches[0]
                character = next(char for char in characters if char["name"] == match)
                return render_template('index.html', 
                                    search_term=search_term, 
                                    ranked_books_tf=ranked_books_tf,
                                    boolean_results=boolean_results,
                                    character=character)
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