# # Open the uploaded file and split it by chapters, creating separate files for each
# input_file_path = 'static/data/05 Harry Potter and the Order of the Phoenix.txt'
# output_dir = 'static/data/'

# # Open the file and read content
# with open(input_file_path, 'r', encoding='utf-8') as file:
#     content = file.read()

# # Define the chapter separator keyword
# chapter_separator = "Chapter 2 -"
# title = "Harry Potter and the Order of the Phoenix"

# # Split the content into chapters based on the keyword
# chapters = content.split(chapter_separator)

# # Save each chapter into a separate file
# output_files = []
# for chapter in chapters[1:]:  # Skip the first split, as it contains pre-chapter text
#     # Extract chapter number and name
#     lines = chapter.strip().split('\n', 1)  # Split into title and rest of the content
#     chapter_title = lines[0].strip()
#     chapter_content = lines[1] if len(lines) > 1 else ''
    
#     # Format file name
#     output_file_name = f"05 {title} - Chapter {chapter_title}.txt"
#     output_file_path = output_dir + output_file_name
    
#     # Save the chapter content to a new file
#     with open(output_file_path, 'w', encoding='utf-8') as output_file:
#         output_file.write(chapter_content)
    
#     # Store the output file path
#     output_files.append(output_file_path)

# output_files


# * Chapter Splitter for Book 5 because for some reason they use a different chapter format
# import re

# # Define the input file path and output directory
# input_file_path = 'static/data/06 Harry Potter and the Half-Blood Prince.txt'
# output_dir = 'static/data/'
# title = "Harry Potter and the Half-Blood Prince"

# # Read the file content
# with open(input_file_path, 'r', encoding='utf-8') as file:
#     content = file.read()

# # Use a regular expression to find all chapter headers
# # Example: "Chapter 2 - A Peck of Owls"
# chapter_pattern = re.compile(r"Chapter \d+ - .+")
# matches = list(chapter_pattern.finditer(content))

# # Extract chapters and save them
# output_files = []
# for i, match in enumerate(matches):
#     # Determine start and end of each chapter's content
#     start_pos = match.start()
#     end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
    
#     # Extract the chapter title and content
#     chapter_title = match.group().replace("Chapter ", "").strip()
#     chapter_content = content[start_pos:end_pos].strip()
    
#     # Format the output file name
#     output_file_name = f"06 {title} - Chapter {chapter_title}.txt"
#     output_file_path = output_dir + output_file_name
    
#     # Save the chapter content into a separate file
#     with open(output_file_path, 'w', encoding='utf-8') as output_file:
#         output_file.write(chapter_content)
    
#     # Store the output file path
#     output_files.append(output_file_path)

# # List the generated files
# print(output_files)

# * Chapter Splitter for Book 6 because AGAIN they use a different chapter format
# Define the file path and output directory based on the uploaded file
input_file_path = 'static/data/06 Harry Potter and the Half-Blood Prince.txt'
output_dir = 'static/data/'
title = "Harry Potter and the Half-Blood Prince"

# Read the file content
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Use a robust regular expression to find all chapter headers
# Example: "Chapter <Number>: <Title>"
import re
chapter_pattern = re.compile(r"Chapter \d+: .+")

# Find all matches for chapter headers
matches = list(chapter_pattern.finditer(content))

# Extract chapters and save them
output_files = []
for i, match in enumerate(matches):
    # Determine the start and end of each chapter's content
    start_pos = match.start()
    end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
    
    # Extract the chapter title and content
    chapter_title = match.group().replace("Chapter ", "").strip()
    chapter_content = content[start_pos:end_pos].strip()
    
    # Format the output file name
    chapter_number, chapter_name = chapter_title.split(": ", 1)
    output_file_name = f"06 {title} - Chapter {chapter_number} - {chapter_name}.txt"
    output_file_path = output_dir + output_file_name
    
    # Save the chapter content into a separate file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(chapter_content)
    
    # Store the output file path
    output_files.append(output_file_path)

output_files
