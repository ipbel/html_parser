import json

import requests
from bs4 import BeautifulSoup
import time

headers = {
    "Content-Language": "en-US"
}


def get_items_urls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    urls = []

    items_urls = soup.find('li',
                           class_='menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-512').find_all(
        'a')
    for item in items_urls[1:]:
        item_url = item.get("href")
        urls.append(item_url)

    with open('item_urls.txt', 'w') as file:
        for i in urls:
            file.write(f'{i}\n')

    return "[URLS] Urls has been successfully collected"


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    count = 1


    for url in urls_list[:4]:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        item_names = []
        try:
            item_name = soup.find_all('h3', class_='elementor-heading-title elementor-size-default')
            for item in item_name:
                item_names.append(item.text.strip())
        except Exception as _ex:
            item_name = None

        items_address = []
        try:
            item_address = soup.find_all('p')
            for i in item_address:
                if "Dirección" in i.text:
                    items_address.append(i.text.replace('Dirección: ', ''))
        except Exception as _ex:
            item_address = None


        items_phones = []
        try:
            item_phones = soup.find_all('p')
            for i in item_phones:
                if "Teléfono" in i.text:
                    items_phones.append(i.text.replace('Teléfono: ', ''))
        except Exception as _ex:
            items_phones = None

        print(len(items_phones))
    # items_working = []
    # try:
    #     item_working = soup.find_all('p')
    #     for i in item_working:
    #         print(i)
    # except Exception as _ex:
    #     items_phones = None


    # for i in range(len(item_names)):
    #     result_list.append(
    #         {
    #             # "name": item_names[i],
    #             "address": items_address[i],
    #             "phones": items_phones[i],
    #         }
    #     )

    # time.sleep(2)
    #
    # print(f'[+] Processed: {count}/{len(urls_list)}')
    #
    # count += 1
    #
    # with open('result.json', 'w') as file:
    #     json.dump(result_list, file, indent=4, ensure_ascii=False)
    #
    # return "[INFO] Data collected successfully!"


def main():
    # print(get_items_urls(url="https://www.santaelena.com.co/"))
    get_data(file_path="item_urls.txt")


if __name__ == "__main__":
    main()
