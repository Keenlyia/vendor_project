# Vendr Scraper

This project automates the process of scraping product data from vendr.com using multithreading and stores it in a PostgreSQL database via Django. All product links and details are fetched and saved.

## 🚀 Features
- Collects product links from selected categories.
- Scrapes product details: name, category, prices, description.
- Saves data in PostgreSQL
- **Multithreading** for faster scraping.

## 🛠️ Requirements
- **Python 3.8+**
- **Django 3.2+**
- **PostgreSQL**
- **Dependencies**: `requests`, `beautifulsoup4`, `threading`, `queue`

## 🔧 Setup

1. **Clone the repository**:  
   ```bash
   https://github.com/Keenlyia/vendor_project.git
   ```
   
2. **Create and activate a virtual environment**:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**:  
   Once the virtual environment is activated, install all required dependencies by running:  
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the database**:  
   Open the `settings.py` file in your Django project and configure your PostgreSQL database connection with the appropriate credentials.

5. **Apply migrations**:  
   Run the following command to apply the necessary database migrations:  
   ```bash
   python manage.py migrate
   ```
6. **Execute the scraper with the following command**:
   ```bash
   python main.py
   ```
