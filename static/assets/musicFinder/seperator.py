import os

# Define the input file path
input_file_path = r'static\assets\musicFinder\lyrics_collection.txt'

# Check if the file exists
if not os.path.exists(input_file_path):
    raise FileNotFoundError(f"The file {input_file_path} was not found.")

# Define the output directory for individual text files
output_dir = '../static/data/musicSongs/'
os.makedirs(output_dir, exist_ok=True)

# Read the input file and split it into individual songs
with open(input_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split the content into blocks for each song based on the separator
songs = content.split("\n" + "="*50 + "\n\n")

# Iterate through each song and save as a separate file
for song in songs:
    lines = song.strip().split("\n")
    if len(lines) < 2:
        continue  # Skip empty or incomplete blocks

    # Extract artist and song name
    artist_line = lines[0] if lines[0].startswith("Artist:") else ""
    song_name_line = lines[1] if lines[1].startswith("Song Name:") else ""
    lyrics = "\n".join(lines[2:])

    # Extract artist and song name values
    artist = artist_line.replace("Artist:", "").strip()
    song_name = song_name_line.replace("Song Name:", "").strip()

    # Create a filename-safe version of the song name
    safe_song_name = "".join(c if c.isalnum() or c.isspace() else "" for c in song_name).strip()
    file_name = f"{safe_song_name}.txt"
    file_path = os.path.join(output_dir, file_name)

    # Write the song data to the file
    with open(file_path, 'w', encoding='utf-8') as song_file:
        song_file.write(f"Artist: {artist}\n")
        song_file.write(f"Song Name: {song_name}\n")
        song_file.write("Lyrics:\n")
        song_file.write(lyrics)

print(f"Songs have been successfully saved to {output_dir}")
