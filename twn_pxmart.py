from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup as bf
import json


class twn_pxmart():
    def __init__(self):
        self.output_pois = []
        self.input_url = "http://www.pxmart.com.tw/px/store1?cityid="

    def run(self,
            export_dir='today',
            backup_dir='bak',
            file_prefix="TWN_POI_Pxmart"):
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
        for idnumber in range(21):
            r=requests.get(self.input_url+str(idnumber)+"&cityzoneid=&cityroadid=&name_short=")
            store_json = json.loads(r.text)
            if len(store_json) == 0:
                continue
            for store in store_json:
                data={}
                data["店名"]=store["name_short"].replace("營業時間：","").replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
                data["電話"]="("+store["tel_zno"]+")"+store["tel_no"].replace("營業時間：","").replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
                data["營業時間"]=store["worktime"].replace("營業時間：","").replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
                if store["address"][0] == "(":
                    data["地址"]=store["address"][7:].replace("營業時間：","").replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
                else:
                    data["地址"]=store["address"].replace("營業時間：","").replace('\r',
                                          ';').replace('\n',
                                                       ';').replace('|', ';')
                data["經度"]=store["mapy"]
                data["緯度"]=store["mapx"]
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
        runner = twn_pxmart()
        runner.run()