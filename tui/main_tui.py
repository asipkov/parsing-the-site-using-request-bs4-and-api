import json
import requests

url = 'https://apigate.tui.ru/api/office/cities'

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.77 Safari/537.36"
}
req = requests.get(url, headers=headers)
scr = req.text

all_cities_id = []
project_data_list = []

dict_scr = json.loads(scr)
values_cities = dict_scr['cities']

for id_ in values_cities:
    all_cities_id.append(id_['cityId'])

for el in all_cities_id:
    url_city = f'https://apigate.tui.ru/api/office/list?cityId={el}&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOp' \
               f'enOnHolidays=false'
    req_city = requests.get(url_city, headers=headers)
    scr_city = req_city.text
    dict_scr_city = json.loads(scr_city)
    values_city = dict_scr_city['offices']
    for one_office in values_city:
        if one_office:
            working_hours = one_office['hoursOfOperation']
            if working_hours['saturday']['isDayOff'] is False and working_hours['sunday']['isDayOff'] is False:
                working_hours_weekend = f'сб {working_hours["saturday"]["startStr"]} до {working_hours["saturday"]["endStr"]}, ' \
                                        f'вс {working_hours["sunday"]["startStr"]} до {working_hours["saturday"]["endStr"]}'
                if working_hours["saturday"]["startStr"] and working_hours["saturday"]["endStr"] == working_hours["sunday"]["startStr"]\
                        and working_hours["saturday"]["endStr"]:
                    working_hours_weekend = f'сб-вс {working_hours["saturday"]["startStr"]} до {working_hours["saturday"]["endStr"]}'
            elif working_hours['saturday']['isDayOff'] is False and working_hours['sunday']['isDayOff'] is True:
                working_hours_weekend = f'сб-вс {working_hours["saturday"]["startStr"]} до {working_hours["saturday"]["endStr"]}'
            else:
                working_hours_weekend = "сб - вс выходной"

            project_data_list.append({
                'address': f'{one_office["address"]}',
                'latlon': f'[{one_office["latitude"]}, {one_office["longitude"]}]',
                'name': f'{one_office["name"]}',
                'phones': f'[{one_office["phones"][0]["phone"]}]',
                'working_hours': f"[пн - пт {working_hours['workdays']['startStr']} до {working_hours['workdays']['endStr']}, "
                                 f"{working_hours_weekend}]",
            }
            )

with open('tui_result.json', 'a', encoding='utf-8') as json_file:
    json.dump(project_data_list, json_file, indent=4, ensure_ascii=False)
