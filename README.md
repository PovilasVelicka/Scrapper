# IKEA Product Scraper

This project is a configurable scraper that downloads products from a single category on the IKEA website.  
It supports multiple storage formats and can resume scraping if interrupted.

---

## 📌 Features

- ✅ Scrapes all paginated products from a selected IKEA category page: https://www.ikea.lt/lt/products  
- ✅ Saves product data in one of the supported formats:
  - SQLite (`.db`)
  - Excel (`.xlsx`)
  - JSONL (`.jsonl`)
- ✅ Automatically resumes from the last successfully scraped item if interrupted  
- ✅ Configurable delay between HTTP requests

---

## 🚀 How to Run (from Scratch)

If you're opening this project for the first time and your computer isn't set up for Python development, follow these steps:

### 1. Install Python

- Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Download and install the latest Python 3 version
- ⚠️ Make sure to check **"Add Python to PATH"** during installation

### 2. Download or Clone the Repository

If you have Git:

```bash
git clone https://github.com/PovilasVelicka/Scrapper.git
cd Scrapper
```

Or download the ZIP from GitHub, extract it, and open the folder in your terminal or command prompt.

### 3. Create Virtual Environment (optional but recommended)

```bash
python -m venv venv
```

Activate it:

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Scraper

Edit the `config.json` file to:

- Set the IKEA category URL to scrape
- Choose the output format
- Configure logging level, delay interval, etc.

Example `config.json`:

```json
{
  "Logging": {
    "LogLevel": "DEBUG"
  },
  "DataBase": {
    "FilePath": ".\\DB\\virtuves-sistema-metod.jsonl"
  },
  "Scrapping":{
    "Url": "https://www.ikea.lt/lt/products/virtuve/virtuves-sistema-metod",
    "Interval": 2
  }
}
```

### 6. Run the Scraper

```bash
python app.py
```

---

## 🪵 Logging

Logging behavior is controlled by the `LogLevel` setting in `config.json`. Example:

```json
"Logging": {
  "LogLevel": "DEBUG"
}
```

Use "DEBUG", "INFO", "WARNING", or "ERROR" depending on how detailed you want the logs. If LogLevel is set to "DEBUG", logging will be done in the console. If set to a higher level, logs will be saved to a file in the logs directory, organized by the date of logging.
