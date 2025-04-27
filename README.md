# Vendr Scraper

This project automates the process of scraping product data from vendr.com using multithreading and stores it in a PostgreSQL database via Django. All product links and details are fetched and saved.

## 🚀 Features
- Collects product links from selected categories.
- Scrapes product details: name, category, prices, description.
- Saves data in PostgreSQL via Django ORM.
- **Multithreading** for faster scraping.

## 🛠️ Requirements
- **Python 3.8+**
- **Django 3.2+**
- **PostgreSQL**
- **Dependencies**: `requests`, `beautifulsoup4`, `threading`, `queue`

## 🔧 Setup

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```
   
