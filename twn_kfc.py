from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup as bf
import json


class twn_kfc():
    def __init__(self):
        self.output_pois = []
        self.input_url = "https://www1.kfcclub.com.tw/tw/ShopSearch/GetShopData"

    def run(self, export_dir='today', backup_dir='bak', file_prefix="TWN_POI_KFC"):
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
        my_data = {
            "data":
            "{\"Method\":\"QueryShopsArea\",\"Addr1\":\"\",\"Addr2\":\"\",\"OtherCondition\":\"\"}"
        }
        r = requests.post(self.input_url, data=my_data)
        soup = bf(r.text, "lxml")
        ls = soup.findAll("p")
        for store in ls:
            data = {}
            data["店名"] = store["name"]
            data["營業時間"] = store["business"]
            data["電話"] = store["phone"]
            data["地址"] = store["addr"]
            data["地點"] = store["remark"].replace("(", "").replace(")", "")
            data["經度"] = store["lon"]
            data["緯度"] = store["lat"]
            if store["break"] == "1":
                data["早餐供應"] = "早餐供應"
            if store["orderway"] == "1":
                data["車道快取"] = "車道快取GO"
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
        runner = twn_kfc()
        runner.run()