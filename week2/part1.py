from bs4 import BeautifulSoup, Comment
from pathlib import Path
import requests as r
import json, csv

towns = ['17821', '17925', '18037', '17975', '17898', '17972']

properties = []

for town in towns:
    soup = BeautifulSoup(
        r.get(
            'https://www.hemnet.se/salda/bostader?location_ids[]={}&sold_age=10m&page=1'.format(town),
            headers={
                "User-Agent": "Popular browser's user-agent"
            }
        )
        .text,
        'html.parser'
    )
    for card in soup.find_all('a', {'class': 'hcl-card'}):
        name_div = card.find_all('div', {'class': lambda x: x and x.startswith('Header_truncate')})
        stats_p = card.find_all('p', {'class': lambda x: x and x.startswith('Text_hclText')})
        fee_div = card.find_all('div', {'class': 'hcl-flex--container hcl-flex--gap-2 hcl-flex--justify-space-between hcl-flex--md-justify-flex-start'})
        price_span = card.find_all('span', {'class': lambda x: x and x.startswith('Text_hclText') and x.startswith('Text_hclTextMedium')})
        location_div = card.find_all('div', {'class': lambda x: x and x.startswith('Location_address')})
        sold_span = card.find_all('span', {'class': lambda x: x and x.startswith('Label_hclLabelSoldAt')})
        type_title = card.find_all('title')

        info_dict = {
            "name": "",
            "Size": "",
            "Room": "?",
            "Fee": "",
            "Endprice": "",
            "KvMPrice": "",
            "Saledate": "",
            "City": "",
            "District": "",
            "TypeOfProperty": "",
            "isValid": False # Just to check if anything has been updated and card is not an ad
        }


        if len(name_div) >  0:
            info_dict["name"] = name_div[0].string
            info_dict["isValid"] = True

        if len(stats_p) > 2:
            info_dict["Size"] = int(float(stats_p[0].string.replace('\xa0', ' ').split(" m²")[0].replace(',', '.')))
            info_dict["Room"] = int(round(float(stats_p[1].string.replace('\xa0', ' ').split(" rum")[0].replace(',', '.'))))
            info_dict["KvMPrice"] = stats_p[2].string.replace('\xa0', ' ').split("kr/")[0]
            info_dict["isValid"] = True

        if len(fee_div) > 0:
            fee_spans = fee_div[0].find_all('span', {'class': lambda x: x and x.startswith('Text_hclText')})
            if len(fee_spans) > 0:
                fee = fee_spans[0].string
                if "kr/mån" in fee:
                    info_dict["Fee"] = fee.split("kr/mån")[0]
                    info_dict["isValid"] = True

        if len(price_span) > 1:
            info_dict["Endprice"] = " ".join(price_span[0].find_all(string=lambda t: not isinstance(t, Comment))).split("Slutpris  ")[1].replace('\xa0', '').split("kr")[0]
            info_dict["isValid"] = True

        if len(location_div) > 0:
            location = location_div[0].span.string.split(', ')
            info_dict["City"] = location[0]
            info_dict["District"] = location[1]
            info_dict["isValid"] = True

        if len(sold_span) > 0:
            info_dict["Saledate"] = sold_span[0].string.split('Såld ')[1]
            info_dict["isValid"] = True

        if len(type_title) > 0:
            info_dict['TypeOfProperty'] = type_title[0].string
            info_dict["isValid"] = True

        if info_dict["isValid"]: # Removes ads from output
            del info_dict["isValid"]
            properties.append(info_dict)



Path("output").mkdir(parents=False, exist_ok=True)

with open("output/housedata2024.csv", "w+") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "Size", "Room", "Fee", "Endprice", "KvMPrice", "Saledate", "City", "District", "TypeOfProperty"])

    writer.writeheader()
    writer.writerows(properties)

with open("output/output.json", "w+") as file:
    file.write(json.dumps(properties))
