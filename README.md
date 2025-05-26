# IKEA Product Scraper

This project is a configurable scraper that downloads products from a single category on the IKEA website.
It supports multiple storage formats and can resume scraping if interrupted.

---

## 📌 Features

- ✅ Scrapes all paginated products from a selected IKEA category page https://www.ikea.lt/lt/products
- ✅ Saves product data in one of the supported formats:
  - SQLite (`.db`)
  - Excel (`.xlsx`)
  - JSONL (`.jsonl`)
- ✅ Automatically resumes from the last successfully scraped item if interrupted
- ✅ Configurable delay between HTTP requests

## 🪵 Logging

Logging behavior is controlled by the `LogLevel` setting in `config.json`. Example:

```json
"Logging": {
    "LogLevel": "DEBUG"
  }

---
