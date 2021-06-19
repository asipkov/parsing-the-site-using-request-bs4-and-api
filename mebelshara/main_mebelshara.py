from bs4 import BeautifulSoup
import json
import requests

url = 'https://www.mebelshara.ru/contacts'

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.77 Safari/537.36"
}
req = requests.get(url, headers=headers)
scr = req.text

with open('mebelshara/mebelshara.html', 'w') as f:
    f.write(scr)

with open('mebelshara/mebelshara.html') as file:
    all_html = file.read()

soup = BeautifulSoup(all_html, 'lxml')

all_city = soup.find_all(class_='city-item')

project_data_list = []

for one_city in all_city:
    while one_city.find(class_='shop-list-item'):
        info_item = one_city.find(class_='shop-list-item')
        working_hours_1 = info_item.get("data-shop-mode1")
        working_hours_2 = info_item.get("data-shop-mode2")
        project_data_list.append({
            'address': f'{one_city.find(class_="js-city-name").text}, {info_item.get("data-shop-address")}',
            'latlon': f'[{info_item.get("data-shop-latitude")}, {info_item.get("data-shop-longitude")}]',
            'name': "Мебель Шара",
            'phones': f'[{info_item.get("data-shop-phone")}]',
            'working_hours': f"[пн - вс {working_hours_2}]" if working_hours_1 == "Без выходных:" else
            f"[{working_hours_1}, {working_hours_2}]",
        }
        )
        info_item.decompose()

with open('mebelshara/mebelshara_result.json', 'a', encoding='utf-8') as json_file:
    json.dump(project_data_list, json_file, indent=4, ensure_ascii=False)
