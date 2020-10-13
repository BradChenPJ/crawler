from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup as bf
import json


class twn_familymart():
    def __init__(self):
        self.output_pois = []
        self.input_url = "https://api.map.com.tw/net/familyShop.aspx?searchType=ShopName&type=&kw=%E5%BA%97&fun=getByName&key=6F30E8BF706D653965BDE302661D1241F8BE9EBC"

    def run(self,
            export_dir='today',
            backup_dir='bak',
            file_prefix="TWN_POI_Familymart"):
        print("start crawler..")
        self.crawler()
        print("data number: " + str(len(self.output_pois)) +
              " , export to csv")
        # backup
        self.export_csv(
            self.output_pois, backup_dir + "/" + file_prefix + '_' +
            datetime.now().strftime("%Y%m%d") + "0000.csv")
        # export
        self.export_csv(
            self.output_pois, export_dir + "/" + file_prefix + '_' +
            datetime.now().strftime("%Y%m%d") + "0000.csv")
        

        print("done!")

    def crawler(self):
        header = {
            "Referer":
            "https://www.family.com.tw/Marketing/inquiry.aspx",
            "Sec-Fetch-Mode":
            "no-cors",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
        r = requests.get(
            self.input_url,
            headers=header)
        soup = bf(r.text, "lxml")
        store_text = soup.find("p").text.replace("getByName(", "").replace(
            "\r", "").replace("\n", "").replace(" ", "")[:-1]
        store_json = json.loads(store_text)
        for store in store_json:
            data = {}
            data["店名"] = store["NAME"].replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
            data["電話"] = store["TEL"].replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
            data["電話2"] = store["POSTel"].replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
            data["店名"] = store["NAME"].replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
            data["郵遞區號"] = store["post"].replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
            data["地址"] = store["addr"].replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
            data["經度"] = store["px"]
            data["緯度"] = store["py"]
            self.output_pois.append(data)

    def export_csv(self, data, csv_filename):
        df = pd.DataFrame(data)
        df.sort_values(df.columns[0], ascending=False).to_csv(csv_filename,
                                                              sep='|',
                                                              encoding='utf-8',
                                                              index=False)
        print('write file: ' + csv_filename)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        runner = twn_familymart()
        runner.run()