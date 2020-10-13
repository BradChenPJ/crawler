from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup as bf
import json
import time


class twn_mcdonald():
    def __init__(self, postcode_path="postcode.csv"):
        self.output_pois = []
        self.input_postcode_path = postcode_path
        self.input_url = "https://www.mcdonalds.com.tw/googleapps/GoogleSearchTaiwanAction.do?method=searchLocation"

    def run(self,
            export_dir='today',
            backup_dir='bak',
            file_prefix="TWN_POI_Mcdonald"):
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
        urlList = [
            "25.0524855%2C%20121.60659250000003",
            "25.1276033%2C%20121.73918329999992",
            "25.0622095%2C%20121.45704469999998",
            "24.9936281%2C%20121.30097980000005",
            "24.8138297%2C%20120.96747519999997",
            "24.774922%2C%20121.04497679999997",
            "24.5631665%2C%20120.81853849999993",
            "24.1631651%2C%20120.67466910000007",
            "24.0517963%2C%20120.51613520000001",
            "23.9609981%2C%20120.97186379999994",
            "23.7092033%2C%20120.4313373",
            "23.4800751%2C%20120.44911130000003",
            "23.5711899%2C%20119.57931570000005",
            "22.9988416%2C%20120.21951480000007",
            "22.6350591%2C%20120.33551929999999",
            "22.5519759%2C%20120.5487597",
            "22.7613207%2C%20121.14381520000006",
            "23.9910732%2C%20121.61119489999999",
            "24.7021073%2C%20121.73775019999994"
        ]

        # postcode
        postcode5 = pd.read_csv(self.input_postcode_path, encoding="utf-8")
        postcode5['zip3'] = [
            str(row['Zip5'])[:3] for i, row in postcode5.iterrows()
        ]
        postcode5 = postcode5.sort_values('zip3').reindex()
        postcode3 = []
        temp_zip3 = ''
        for i, row in postcode5.iterrows():

            if i == 0 or temp_zip3 != row['zip3']:
                temp_zip3 = row['zip3']
                postcode3.append({
                    "zip3": row['zip3'],
                    "City": row['City'],
                    "Area": row['Area']
                })
        postcode3 = pd.DataFrame(postcode3)
        for coor in urlList:
            url = self.input_url + "&searchTxtLatlng=" + coor + "&actionType=filterRestaurant&language=zh&country=tw"
            print("crawling page: " + url)
            time.sleep(3)
            r = requests.get(url)
            store_json = json.loads(r.text)
            for store in store_json["results"]:
                try:
                    data = {}
                    data["店名"] = store["name"].strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
                    data["電話"] = store["telephone"].strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
                    address = store["addresses"][0]["address"].split(
                        ",")[0].replace("<h3>", "").replace("</h3>",
                                                            "").strip()
                    postcode = address[:3]
                    data["地址raw"] = address.replace('\r', ';').replace(
                        '\n', ';').replace('|', ';')
                    data["地址filered"] = address[3:].strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
                    data["經度"] = store["longitude"]
                    data["緯度"] = store["latitude"]
                    data["營業時間"] = store["timeings"][1][
                        "openTime"] + "~" + store["timeings"][
                            1]["closeTime"].replace('\r', ';').replace(
                                '\n', ';').replace('|', ';')
                    if len(postcode3[postcode3['zip3'] == postcode].City) > 0:
                        data["cityFromzip3"] = list(postcode3[
                            postcode3['zip3'] == postcode]['City'])[0]
                        data["townFromzip3"] = list(postcode3[
                            postcode3['zip3'] == postcode]['Area'])[0]

                    if data in self.output_pois:
                        continue
                    self.output_pois.append(data)
                except:
                    if data in self.output_pois:
                        continue
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
        runner = twn_mcdonald()
        runner.run()