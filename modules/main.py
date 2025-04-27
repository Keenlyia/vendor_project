from parser import get_all_product_links
from scraper import scrape_products

def main():
    """ Основна функція запуску парсера"""
    all_links = get_all_product_links()
    scrape_products(all_links)
    print('✅ Done!')

if __name__ == "__main__":
    main()