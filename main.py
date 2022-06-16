import json
import requests
from bs4 import BeautifulSoup as BeautifulSoup


headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '53.0.2785.143 Safari/537.36'
    }
url = "http://masterskaya-sporta.ru/katalog/sila-i-massa/proteini/sivorotochniy/?show=100&ajax_filter=1&no_open=1&use_path=1&is_webp=1"
url_items = []
info_items = []


def main():
    parser = requests.get(url, headers=headers)

    parser_html = BeautifulSoup(parser.content, "html.parser")
    items = parser_html.find_all("div", class_="list-tile-flex-top")
    for item in items:
        try:
            url_item = "http://masterskaya-sporta.ru" + item.find("a").get("href")
            url_items.append(url_item)
        except Exception:
            url_item = "No info"

    with open("uml_item.json", "w") as file:
        json.dump(url_items, file, indent=4, ensure_ascii=False)

    with open("uml_item.json") as file:
        url_items_all = json.load(file)
    i = 0
    for url_item in url_items_all:
        print("Загрузка объекта :" + str(i))
        i += 1
        parser_item = requests.get(url_item, headers=headers)
        parser_item_content = BeautifulSoup(parser_item.content, "html.parser")
        name_item = parser_item_content.find("h1").get_text(strip=True)

        price_item = parser_item_content.find("span", class_="price-propria").get_text(strip=True)

        brand_item = parser_item_content.find("tr", class_="catalog-model-brand-row").find("a").get_text(strip=True)

        country_item = parser_item_content.find("div", class_="catalog-model-brand-location").get_text(strip=True)
        try:
            weight_item = str(parser_item_content.find("div", id="catalog-distinct-params").get_text(strip=True)).replace("Вес: ", "")
        except Exception:
            weight_item = ""

        info_items.append({
            "Название продукта": name_item,
            "Цена": price_item,
            "Вес": weight_item,
            "Бренд": brand_item,
            "Страна производитель": country_item
        })
    with open("info_item.json", "a", encoding="utf=8") as file_json:
        json.dump(info_items, file_json, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()

