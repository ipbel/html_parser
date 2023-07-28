import json

import requests
from bs4 import BeautifulSoup
import time

headers = {

}


def get_items_urls(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    urls = [url + 'about']

    items_urls = soup.find("div", class_="site-header__right").find("div", class_="city-select__list").find_all("a")
    for item in items_urls:
        item_url = item.get("href")
        urls.append(item_url + '/about')

    with open('item_urls.txt', 'w') as file:
        for i in urls:
            file.write(f'{i}\n')

    return "[URLS] Urls has been successfully collected"


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    count = 1

    for url in urls_list[:3]:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        items_address = []
        try:
            city = soup.find("div", class_="site-footer__address-list").find_all('h2')[1].text.strip(':')
            item_address = soup.find("div", class_="site-footer__address-list").find_all("li")

            for address in item_address:
                items_address.append(city + ', ' + address.text.replace("\u200b", ""))
        except Exception as _ex:
            item_address = None

        try:
            item_phone = soup.find("div", class_="contacts__phone").find("a").get("href")[4:]
        except Exception as _ex:
            item_phone = None

        result_list.append(
            {
                "name": "Японский Домик",
                "addess": items_address,
                "phone": item_phone
            }
        )


    print(soup.find_all('script')[3].text.strip('window.initialState = '))

    #     time.sleep(2)
    #     print(f'[+] Processed: {count}/{len(urls_list)}')
    #
    #     count += 1
    #
    #
    # with open('result.json', 'w') as file:
    #     json.dump(result_list, file, indent=4, ensure_ascii=False)

    return "[INFO] Data collected successfully!"


def main():
    print(get_items_urls(url="https://omsk.yapdomik.ru/"))
    # print(get_data(file_path="item_urls.txt"))


if __name__ == "__main__":
    main()
