import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
import re

from load_django import *
from parser_app.models import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_product_details(product_url):
    """Завантажує та парсить детальну інформацію про продукт за його URL."""
    full_product_url = f'https://www.vendr.com{product_url}'
    print(f"Отримую дані з продукту: {full_product_url}")
    response = requests.get(full_product_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        product_name = soup.find('h1', class_='rt-Heading rt-r-size-6 xs:rt-r-size-8').text
    except AttributeError:
        product_name = None

    try:
        category_elements = soup.find_all("a", class_="rt-Text rt-reset rt-Link rt-r-size-1 rt-underline-auto")
        categories = [category.find("span").text for category in category_elements]
        index_of_categories = categories.index('Categories')  # Find the index of 'Categories'
        category = categories[index_of_categories + 1]
    except (ValueError, AttributeError):
        category = None

    try:
        low_price_tag = soup.find('span', class_='v-fw-600 v-fs-12').text
        low_price = re.sub(r'[^0-9.]', '', low_price_tag)
    except AttributeError:
        low_price = None

    try:
        high_price_tag = soup.find('span', class_='_rangeSliderLastNumber_118fo_38 v-fw-600 v-fs-12').text
        high_price = re.sub(r'[^0-9.]', '', high_price_tag)
    except AttributeError:
        high_price = None

    try:
        median_price_tag = soup.find('div', class_='rt-Flex _rangeAverage_118fo_42').text
        median_price = re.sub(r'[^0-9.]', '', median_price_tag)
    except AttributeError:
        median_price = None

    try:
        description = soup.find('div', class_='rt-Box _read-more-box__content_122o3_1').text
    except AttributeError:
        description = None

    product, created = Product.objects.update_or_create(
        name=product_name,
        defaults={
            'category': category,
            'low_price': low_price,
            'high_price': high_price,
            'median_price': median_price,
            'description': description
        }
    )

    return product


def worker(queue):
    """Працює, поки черга не стане порожньою."""
    while not queue.empty():
        product_url = queue.get()
        product = get_product_details(product_url)
        queue.task_done()


def scrape_products(all_links):
    """Створює кілька потоків (10 за замовчуванням), кожен з яких обробляє URL"""
    queue = Queue()

    for url in all_links:
        queue.put(url)

    # Створюємо кілька потоків для обробки
    num_threads = 10
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=worker, args=(queue,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
