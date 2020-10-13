from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup as bf
import json


class twn_domino():
    def __init__(self):
        self.output_pois = []
        self.input_url = "https://www.dominos.com.tw/storec_"

    def run(self,
            export_dir='today',
            backup_dir='bak',
            file_prefix="TWN_POI_Domino"):
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
        for i in range(82900, 83300):
            r = requests.get(self.input_url + str(i) + ".htm")
            soup = bf(r.text, "lxml")
            info = soup.find("div", id="shop_info").findAll("div")
            if len(info) == 1:
                continue
            data = {}
            print(i)
            try:
                data["店名"] = soup.find("div",
                                       id="shop_name").find("h3").text.replace(
                                           '\r',
                                           ';').replace('\n',
                                                        ';').replace('|', ';')
                data["電話"] = soup.find("div", id="shop_tel").text.replace(
                    '\r', ';').replace('\n', ';').replace('|', ';')
                data["地址"] = soup.find("div", id="shop_add").text.replace(
                    '\r', ';').replace('\n', ';').replace('|', ';')
                data["營業時間"] = soup.find(
                    "div", id="opening").find("span").text.replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
            except:
                print("go")
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
        runner = twn_domino()
        runner.run()