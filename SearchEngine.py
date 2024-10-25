import os
import re

# Load Data
data_dir = 'data'
books = {}

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
            books[filename] = file.read()

# Define a set of stop words
stop_words = set([
    'the', 'in', 'of', 'and', 'to', 'a', 'is', 'it', 'that', 'on', 'for', 
    'as', 'with', 'was', 'at', 'by', 'an', 'be', 'this', 'are', 'from', 
    'but', 'not', 'or', 'he', 'she', 'they', 'his', 'her', 'its', 'if', 
    'what', 'which', 'who', 'when', 'where', 'why', 'all', 'any', 'some'
])

# Preprocess text to handle punctuation and possessives
def preprocess_text(text):
    text = text.lower()
    # Remove punctuation by keeping only word characters and spaces between them
    words = re.findall(r'\b\w+\b', text)
    # Filter out stop words
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# Preprocess each book
processed_books = {title: preprocess_text(content) for title, content in books.items()}

# Function to count occurrences of a single word in text
def count_single_word(text, word):
    word = word.lower()  # Ensure case-insensitive search
    # Use word boundaries to match whole words only
    return len(re.findall(r'\b' + re.escape(word) + r'\b', text))

# Function to count total occurrences of all words in the search term
def count_occurrences(text, search_term):
    search_words = search_term.lower().split()  # Split search term into individual words
    total_count = sum(count_single_word(text, word) for word in search_words)  # Sum the counts of all words
    return total_count

# Function to search and rank books based on total occurrences of all words in the search term
def search_books_tf(books, search_term):
    occurrences = {}
    
    for title, text in books.items():
        occurrence_count = count_occurrences(text, search_term)
        occurrences[title] = occurrence_count
    
    # Sort books by occurrence count in descending order
    ranked_books = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    
    return ranked_books

# Boolean retrieval function
def boolean_retrieval(books, query):
    results = {}
    
    # Normalize and split the query
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)
    
    # Initialize a list for matching titles
    for title, text in books.items():
        matches = True
        for token in tokens:
            # Handle NOT operator
            if token.startswith("not "):
                search_term = token[4:]  # Get the term after NOT
                if count_single_word(text, search_term) > 0:
                    matches = False
                    break
            else:
                # Normal AND behavior
                if count_single_word(text, token) == 0:
                    matches = False
                    break
        
        if matches:
            results[title] = matches
            
    return results

# Example searches
tf_search_term = "harry potter"
ranked_books_tf = search_books_tf(processed_books, tf_search_term)

boolean_search_term = "harry potter"
boolean_results = boolean_retrieval(processed_books, boolean_search_term)

# Displaying the results for TF
print("TF Ranking of books based on occurrences of the search term : " + tf_search_term)
for title, count in ranked_books_tf:
    print(f"{title}: {count} occurrences")

# Displaying the results for Boolean retrieval
print("\nBoolean Retrieval Results:")
for title in boolean_results:
    print(f"{title}: matches the query")
    
