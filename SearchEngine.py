from flask import Flask, render_template, request
import os
import re
import webbrowser

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
    'will', 'just', 'don', 'should', 'now'
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