import requests
from bs4 import BeautifulSoup
from selenium import webdriver

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en",
}


def get_source_html(url):
    driver = webdriver.Chrome()
    driver.get(url=url)

    with open("source-page.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)


def get_items_urls(file_path):
    with open(file_path) as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("section",
                               class_="elementor-section elementor-inner-section elementor-element elementor-element-01a0b47 LinkToClinic elementor-section-boxed elementor-section-height-default elementor-section-height-default")

    urls = []
    for item in items_divs:
        item_url = item.find("a").get("href")
        urls.append(item_url)

    with open('items_urls.txt', 'w') as file:
        for url in urls:
            file.write(f'{url}\n')

    return "[URLS] Urls has been successfully collected"


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    for url in urls_list[:1]:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        # try:
        item_name = soup.find()
        # except Exception as _ex:
        #     item_name = None
        print(soup)


def main():
    # get_source_html(url='https://dentalia.com/')
    # print(get_items_urls(file_path="source-page.html"))
    print(get_data(file_path="items_urls.txt"))


if __name__ == "__main__":
    main()
