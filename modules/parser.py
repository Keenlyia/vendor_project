import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

def get_updated_category_urls():
    """Отримує оновлені URL-адреси продуктів з трьох категорій"""
    categories = [
        "https://www.vendr.com/categories/devops",
        "https://www.vendr.com/categories/it-infrastructure",
        "https://www.vendr.com/categories/data-analytics-and-management"
    ]
    all_category_urls = []
    for url in categories:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        category_urls = [category.find('a').get("href") for category in soup.find_all("div", class_="rt-Box rt-r-pb-1") if category.find('a')]
        all_category_urls.extend(category_urls)
    updated_category_urls = [url.split('?')[0] + '?' + '&'.join(url.split('?')[1:]).split('&')[0] + '&' for url in all_category_urls]
    return updated_category_urls

def get_product_links(category_url, page_num):
    """Знаходить усі посилання на окремі продукти"""
    full_url = f'https://www.vendr.com{category_url}page={page_num}'
    print(f"Отримую сторінку: {full_url}")
    response_url = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response_url.text, "html.parser")
    links = [link.get('href') for link in soup.find_all('a', class_='_card_j928a_9 _card_1u7u9_1 _cardLink_1q928_1')]
    print(f"Знайдено {len(links)} посилань на сторінці {page_num}")
    return links

def worker(queue, all_links):
    """Для кожної категорії по черзі перебирає сторінки (page_num)."""
    while not queue.empty():
        category_url = queue.get()
        page_num = 1
        while True:
            links = get_product_links(category_url, page_num)
            if not links:
                break
            all_links.extend(links)
            page_num += 1
        queue.task_done()

def get_all_product_links():
    """Створює потоки, повертає зібраний список всіх посилань на продукти."""
    updated_category_urls = get_updated_category_urls()
    all_links = []
    queue = Queue()

    # Додаємо URL категорій у чергу
    for category_url in updated_category_urls:
        queue.put(category_url)

    # Створюємо два потоки
    threads = []
    for _ in range(2):
        thread = Thread(target=worker, args=(queue, all_links))
        threads.append(thread)
        thread.start()

    # Чекаємо завершення всіх потоків
    for thread in threads:
        thread.join()

    return all_links