from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup as bf
import json


class twn_carrefour():
    def __init__(self):
        self.output_pois = []
        self.input_url = "https://www.carrefour.com.tw/api/Store"

    def run(self,
            export_dir='today',
            backup_dir='bak',
            file_prefix="TWN_POI_Carrefour"):
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
        r = requests.get(self.input_url)

        store_json = json.loads(r.text)
        for store in store_json["result"]:
            data = {}
            data["中文名稱"] = str(store["分店中文名稱"]).replace('\r', ';').replace(
                '\n', ';').replace('|', ';')
            data["英文名稱"] = str(store["分店英文名稱"]).replace('\r', ';').replace(
                '\n', ';').replace('|', ';')
            data["電話號碼"] = str(store["電話號碼"]).replace('\r', ';').replace(
                '\n', ';').replace('|', ';')
            data["營業時間"] = str(store["營業時間"]).replace('\r', ';').replace(
                '\n', ';').replace('|', ';')
            data["地址"] = str(store["縣市"]) + str(store["區"]) + str(
                store["地址"]).replace('\r', ';').replace('\n', ';').replace(
                    '|', ';')
            data["經度"] = store["Longitude"]
            data["緯度"] = store["Latitude"]
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
        runner = twn_carrefour()
        runner.run()