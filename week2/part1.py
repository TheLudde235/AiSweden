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
            "name": "No name found",
            "size": "No size found",
            "room": "No room found",
            "fee": "No fee found",
            "endprice": "No Endprice found",
            "kvMPrice": "No KvMPrice found",
            "saledate": "No Saledate found",
            "city": "No City found",
            "district": "No District found",
            "typeOfProperty": "No TypeOfProperty found",
            "isValid": False # Just to check if anything has been updated and card is not an ad
        }


        if len(name_div) >  0:
            info_dict["name"] = name_div[0].string
            info_dict["isValid"] = True

        if len(stats_p) > 2:
            info_dict["size"] = stats_p[0].string.replace('\xa0', ' ')
            info_dict["room"] = stats_p[1].string.replace('\xa0', ' ')
            info_dict["kvMPrice"] = stats_p[2].string.replace('\xa0', ' ')
            info_dict["isValid"] = True

        if len(fee_div) > 0:
            fee_spans = fee_div[0].find_all('span', {'class': lambda x: x and x.startswith('Text_hclText')})
            if len(fee_spans) > 0:
                fee = fee_spans[0].string
                if "kr/mån" in fee:
                    info_dict["fee"] = fee
                    info_dict["isValid"] = True

        if len(price_span) > 1:
            info_dict["endprice"] = " ".join(price_span[0].find_all(string=lambda t: not isinstance(t, Comment))).split("Slutpris  ")[1].replace('\xa0', ' ')
            info_dict["isValid"] = True

        if len(location_div) > 0:
            location = location_div[0].span.string.split(', ')
            info_dict["city"] = location[0]
            info_dict["district"] = location[1]
            info_dict["isValid"] = True

        if len(sold_span) > 0:
            info_dict["saledate"] = sold_span[0].string.split('Såld ')[1]
            info_dict["isValid"] = True

        if len(type_title) > 0:
            info_dict['typeOfProperty'] = type_title[0].string
            info_dict["isValid"] = True

        if info_dict["isValid"]: # Removes ads from output
            del info_dict["isValid"]
            properties.append(info_dict)



Path("output").mkdir(parents=False, exist_ok=True)

with open("output/output.csv", "w+") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "size", "room", "fee", "endprice", "kvMPrice", "saledate", "city", "district", "typeOfProperty"])
    writer.writeheader()
    writer.writerows(properties)

with open("output/output.json", "w+") as file:
    file.write(json.dumps(properties))
