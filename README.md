# 🚀 SEARCH ENGINE PROJECT (Sistem Temu Balik Informasi)

## 📖 DESCRIPTION
This project is a **search engine web application built with Flask**, implemented using **two separate Python scripts**, each serving a different dataset and functionality:

- 📚 **`SearchEngine.py`**: A search engine for **Harry Potter books & characters**.  
  Includes boolean retrieval, term frequency ranking, stopword removal, and approximate character name matching using Levenshtein distance.

- 🎵 **`MusicSearchEngine.py`**: A search engine for **song lyrics**.  
  Includes boolean retrieval, term frequency ranking, and stopword removal.

Both engines are independent and provide their own web interfaces.  
This project demonstrates core *Information Retrieval (IR)* concepts, *Text Preprocessing*, and *Web Deployment with Flask*.

---

# 🛠️ TECHNOLOGIES
- Python 3
- Flask
- HTML / Jinja2 templates
- [python-Levenshtein](https://pypi.org/project/python-Levenshtein/) (used in `SearchEngine.py`)

---

# 🚀 GETTING STARTED

## 📥 Clone the repository
```bash
git clone https://github.com/Irvandmw/SearchEngineOptimizationProject.git
cd SearchEngineOptimizationProject
```

## 📦 INSTALL DEPENDENCIES
```bash
pip install flask python-Levenshtein
```

## 🗂️ PREPARE DATASETS
📚 Book & Character Mode (SearchEngine.py)
- Place .txt book files in:
  ```bash
  static/data/
  ```

- Place characters.json in:
  ```bash
  static/assets/characters/
  ```

## ▶️ RUN THE ENGINES

### 📚 Run Harry Potter Search Engine

```bash
python SearchEngine.py
```
The browser will automatically open at:
```bash
http://127.0.0.1:5000/
```

### 🎵 Run Music Lyrics Search Engine
```bash
python MusicSearchEngine.py
```

The browser will automatically open at:
```bash
http://127.0.0.1:5000/
```

## 🔍 SEARCH FEATURES

### 📚 Book & Character Mode (`SearchEngine.py`)

- **Boolean Retrieval**: Finds books containing all query terms.
- **Term Frequency Ranking**: Ranks books by frequency of query terms.
- **Stopword Removal**: Removes common stopwords for relevance.
- **Approximate Character Matching**: Suggests the closest character name for misspelled queries using Levenshtein distance.
- **Reading Mode**: Displays the full book content.

### 🎵 Music Lyrics Mode (`MusicSearchEngine.py`)

- **Boolean Retrieval**: Finds songs containing all query terms.
- **Term Frequency Ranking**: Ranks songs by frequency of query terms.
- **Stopword Removal**: Removes common stopwords.
- **Reading Mode**: Displays the full song lyrics.

## 🧪 EXAMPLE QUERIES

### SearchEngine.py
<img width="1920" height="1163" alt="image" src="https://github.com/user-attachments/assets/1e645297-f3e0-44f4-829b-f9861033f07b" />
<img width="1920" height="1160" alt="image" src="https://github.com/user-attachments/assets/df9bb8bd-50b5-4ff1-a030-ad14a11c4f47" />

### MusicSearchEngine.py
<img width="1920" height="1160" alt="image" src="https://github.com/user-attachments/assets/48683a24-01f8-41df-8c9d-fc179e601ab1" />
<img width="1920" height="1160" alt="image" src="https://github.com/user-attachments/assets/57689e53-7e3f-48c6-b117-6cb5775a7f6f" />

## 📜 LICENSE

This project is shared with the intention to help others learn and explore.  
You are welcome to use, modify, or extend this project for your own educational or personal purposes.  

However, if you do use this project in any way,  
**please kindly include proper credit to the original author by mentioning:**

🔗 Contact: 
- [Irvan](https://github.com/Irvandmw)
- [Rafael Joy Hadi](https://github.com/rafaeljoyhadi)
- [Carollyn Thio](https://github.com/ollynth)

Giving credit helps acknowledge the effort behind this work and supports open collaboration.  
Thank you for respecting the creator’s contribution! 🌱

