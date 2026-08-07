# 😊 Sentiment Analysis CLI

A **Python-based Sentiment Analysis CLI** that analyzes text as **Positive, Negative, or Neutral** using **NLTK's VADER sentiment analyzer**. The application follows a modular architecture with persistent JSON storage for analysis history and works offline after the initial VADER lexicon download.

---

# 📌 Overview

The Sentiment Analysis CLI is a command-line application that evaluates the sentiment of user-provided text or text files. It classifies text into **Positive**, **Negative**, or **Neutral** sentiment while maintaining a history of previous analyses. The project follows a clean modular architecture by separating the user interface, business logic, data models, and storage layer.

---

# ✨ Features

- 😊 Analyze a single sentence
- 📄 Analyze multiple sentences from a text file
- 📊 Detect Positive, Negative, or Neutral sentiment
- 📜 View analysis history
- 📈 Display sentiment statistics
- 🗑️ Clear analysis history
- 💾 JSON-based persistent storage
- ⚡ Offline sentiment analysis using VADER
- 🖥️ Menu-driven Command-Line Interface (CLI)

---

# 🛠️ Technologies Used

- **Python**
- **NLTK (VADER Sentiment Analyzer)**
- **JSON**
- **Object-Oriented Programming (OOP)**
- **Command-Line Interface (CLI)**
- **Modular Programming**

---

# 📁 Project Structure

```text
Sentiment-Analysis-CLI/
│
├── main.py                    # Application entry point
├── cli.py                     # User interface and menu
├── service.py                 # Sentiment analysis logic
├── repository.py              # JSON storage management
├── models.py                  # Data models
├── sentiment_history.json     # Analysis history
├── Purpose.md                 # Project description
└── workingPrinciple.txt       # Working principle
```

---

# 📖 Workflow

```text
Program Start
      │
      ▼
main.py
      │
      ▼
Initialize Repository
      │
      ▼
Initialize Sentiment Service
      │
      ▼
Launch CLI
      │
      ▼
Display Main Menu
      │
      ├── Analyze Single Sentence
      ├── Analyze Text File
      ├── View History
      ├── View Statistics
      ├── Clear History
      └── Exit
      │
      ▼
Analyze Sentiment
      │
      ▼
Save Result to JSON
      │
      ▼
Return to Main Menu
```

---

# 🚀 How to Run

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Install Required Package

```bash
pip install nltk
```

### 3. Run the Application

```bash
python main.py
```

---

# 🔄 Data Flow

```text
User Input
     │
     ▼
cli.py
     │
     ▼
service.py
     │
     ▼
models.py
     │
     ▼
repository.py
     │
     ▼
sentiment_history.json
```

---

# 📂 Module Responsibilities

### 📄 main.py
- Initializes the application and connects all modules.

### 📄 cli.py
- Provides the interactive command-line interface.
- Handles user input and menu navigation.

### 📄 service.py
- Performs sentiment analysis using VADER.
- Generates statistics and manages analysis history.

### 📄 repository.py
- Reads and writes analysis history to JSON.

### 📄 models.py
- Defines sentiment data models and analysis results.

### 📄 sentiment_history.json
- Stores analysis history for future reference.

---

# 🔮 Future Improvements

- 🖥️ GUI using Tkinter or PyQt
- 📊 Sentiment visualization with graphs
- 🌍 Multi-language sentiment analysis
- 🤖 Machine Learning-based sentiment classification
- 🗄️ SQLite/MySQL database integration
- 📄 PDF report generation
- ☁️ Cloud synchronization

---

# 👨‍💻 Author

**Swopnil Biswas**

B.Tech – Electronics & Communication Engineering

---

⭐ **A practical Python project built to strengthen Object-Oriented Programming, modular programming, JSON data handling, and Natural Language Processing (NLP) using NLTK's VADER sentiment analyzer.**
