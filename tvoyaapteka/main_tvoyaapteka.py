from bs4 import BeautifulSoup
import json
import requests

url = 'https://www.tvoyaapteka.ru/adresa-aptek/'

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.77 Safari/537.36"
}
req = requests.get(url, headers=headers)
scr = req.text
soup = BeautifulSoup(scr, 'lxml')

all_towns = soup.find_all(class_='town_xs_item')
id_towns = []
for el in all_towns:
    one_id_town = el.get('data-id')
    if one_id_town is None:
        pass
    else:
        id_towns.append(one_id_town)

project_data_list = []

for id_town in id_towns:
    cookie = {'Cookie':'PHPSESSID=8h67o5hpmqtu6jc9trfhhtbgeq; BITRIX_SM_H2O_COOKIE_USER_ID=465876300ee18aa632cb965fcd54c48c; '
                     'BITRIX_SM_GEOIP=a:2:{s:7:"inetnum";s:27:"46.216.0.0+-+46.216.255.255";s:7:"country";s:2:"BY";}; '
                     'BITRIX_SM_LAST_IP=46.216.153.117; BITRIX_SM_SP_deviceId=2021-06-16_05:54:07_2da5f95677992781544f3c555a2bea91;'
                     ' _ym_uid=1623790450821578018; _ym_d=1623790450; tmr_lvid=7b87acb553b20e9fa36430c26d43dd61; '
                     'tmr_lvidTS=1623790450551; __utmc=202854356; BX_USER_ID=ad122ace23755d60cb4bc761674105d6; '
                     'BITRIX_SM_SALE_UID=3569043; _gid=GA1.2.728250922.1624049538; __utmz=202854356.1624119182.7.2.utmcsr'
                     '=yandex|utmccn=(organic)|utmcmd=organic; ct_visible_fields=0; ct_visible_fields_count=0; _ym_isad=1;'
                     ' BITRIX_SM_S_CITY_ID='+ id_town +'; ct_prev_referer=https://www.tvoyaapteka.ru/; '
                     'ct_checkjs=d8f681da098da56878f541f558036d5f; __utma=202854356.815192023.1623790445.1624123016.'
                     '1624137733.9; ct_timestamp=1624138557; ct_cookies_test={"cookies_names":["ct_timestamp","ct_prev_referer"],'
                     '"check_value":"a1325bddada904ce53656fdf31868890"}; ct_ps_timestamp=1624138558; __utmb=202854356.2.9.1624138558721;'
                     '_ga=GA1.2.815192023.1623790445; _dc_gtm_UA-73974408-1=1; _gat_gtag_UA_189291181_1=1; tmr_detect=1|1624138558776;'
                     '_gat_UA-73974408-1=1; ct_timezone=3; ct_fkp_timestamp=1624138559; _ga_HLYRZD8M17=GS1.1.1624137732.9.1.1624138573.44;'
                     'ct_pointer_data=[[167,533,324],[219,511,498],[230,506,505],[260,490,630],[237,479,786],[219,471,946],[205,452,1367],'
                     '[489,580,3804],[470,619,3920],[258,871,4070],[238,898,4270],[234,910,4370],[203,970,4552],[199,1018,4856],'
                     '[200,1018,4861],[202,1016,5025],[204,1014,5183],[200,1013,5279],[361,777,5409],[376,299,20169],[159,268,20261],'
                     '[123,264,20419],[26,509,20564],[26,516,21042],[20,515,21596],[22,506,21612],[3,66,22273],[231,103,22369],'
                     '[362,97,22509],[377,52,23409],[116,78,23565],[11,83,23712],[3,83,23875]]; tmr_reqNum=226'}
    one_city_html = requests.get('https://www.tvoyaapteka.ru/adresa-aptek/', cookies=cookie).text
    soup = BeautifulSoup(one_city_html, 'lxml')
    info = soup.find_all(class_='apteka_item normal_store')
    for el in info:
        working_hours = el.find(class_="apteka_time").find("span").text
        working_hours = working_hours.replace('\t', '').replace('\n', '')
        project_data_list.append({
                        'address': f'{el.find(class_="apteka_address").find("span").text}',
                        'latlon': f'[{el.get("data-lat")}, {el.get("data-lon")}]',
                        'name': f'{el.find(class_="apteka_title").find("span").text}',
                        'phones': '[+78001000003]',
                        'working_hours': f'{working_hours}',
                    }
                    )

with open('tvoyaapteka_result.json', 'a', encoding='utf-8') as json_file:
    json.dump(project_data_list, json_file, indent=4, ensure_ascii=False)
