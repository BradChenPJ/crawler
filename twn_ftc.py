import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
from datetime import datetime


class twn_ftc:
    def __init__(self):
        self.output_pois = []
        self.input_url = "http://ftc.com.tw/oil/gettotalstation.asp"

    def run(self,
            export_dir="today",
            backup_dir="bak",
            file_prefix="TWN_POI_FTC"):
        self.crawler()
        self.export_csv(
            self.output_pois, backup_dir + "/" + file_prefix + '_' +
            datetime.now().strftime("%Y%m%d") + "0000.csv")
        # export
        self.export_csv(
            self.output_pois, export_dir + "/" + file_prefix + '_' +
            datetime.now().strftime("%Y%m%d") + "0000.csv")

    def crawler(self):
        r = requests.get(self.input_url)
        r.encoding = 'big5'
        soup =bf(r.text, "lxml")
        tr = soup.find("table").findAll("tr")
        for each_tr in tr[2:]:
            data = {}
            data["名稱"] = each_tr.findAll("td")[1].text.strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
            data["電話"] = each_tr.findAll("td")[3].text.strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
            data["地址"] = each_tr.findAll("td")[2].text.strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
            oil_type = []
            for item in each_tr.findAll("td")[4]:
                oil_type.append(item['src'].replace('jpg','').replace('.','').replace('o','').replace('/',''))
            data["販售油品種類"] = ";".join(oil_type)
            data["自助"] = each_tr.findAll("td")[5].text.strip().replace(
                        '\r', ';').replace('\n', ';').replace('|', ';')
            self.output_pois.append(data)

    def export_csv(self, data, csv_filename):
        df = pd.DataFrame(data)
        df.sort_values(df.columns[0], ascending=False).to_csv(csv_filename,
                                                              sep='|',
                                                              encoding='utf-8',
                                                              index=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        runner = twn_ftc()
        runner.run()