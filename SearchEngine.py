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

# Preprocess text to handle punctuation and possessives
def preprocess_text(text):
    text = text.lower()
    # Remove punctuation by keeping only word characters and spaces between them
    words = re.findall(r'\b\w+\b', text)
    # Filter out stop words
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# # Function to count occurrences of a single word in text
def count_single_word(text, word):
    word = word.lower()
    return len(re.findall(r'\b' + re.escape(word) + r'\b', text))

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

# Function to remove stop words from text
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

# Preprocess each book
processed_books = {title: preprocess_text(content) for title, content in books.items()}

# Preprocess each book
processed_books = {title: preprocess_text(content) for title, content in books.items()}

# Function to count occurrences of a multi-word search term
def count_occurrences(text, search_term):
    # Count the number of times the search term appears in the text
    return text.lower().count(search_term.lower())

character_corrections = {
    "harry" : ["hary"],
    "potter": ["poter", "pottr", "poterr"]
}

def correct_search_term(search_term):
    # Normalize the search term to lowercase
    normalized_term = search_term.lower()
    
    # Check if the search term matches any of the known misspellings
    for correct_term, misspellings in character_corrections.items():
        if normalized_term in misspellings:
            return correct_term  # Return the correct term if a misspelling is found
    # If no match, return the original term
    return normalized_term

# Updated search_books function to include spelling correction
def search_books(books, search_term):
    # Preprocess the corrected search term to remove stop words
    processed_search_term = remove_stop_words(search_term.lower())
    
    # Split the processed search term into individual words
    search_words = processed_search_term.split()
    
    # Correct the search term for known character names
    corrected_search_term = [correct_search_term(term) for term in search_words]

    occurrences = {}
    
    for title, text in books.items():
        # Initialize count for each book
        occurrence_count = 0
        
        # Count occurrences of each word in the search words
        for word in corrected_search_term:
            occurrence_count += count_occurrences(text, word)
        
        occurrences[title] = occurrence_count
    
    # Sort books by occurrence count in descending order
    ranked_books = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    
    return ranked_books    

# FLASK
# http://127.0.0.1:5000/
# Go to the above URL to run the search engine in your browser
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        ranked_books_tf = search_books(processed_books, search_term)
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