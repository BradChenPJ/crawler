import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
import time
import numpy as np
#gov=[]
#name=[]
#nameLink=[]
#dic={}
def table(URL):
    data_list=[]
    r = requests.get(URL)
    time.sleep(0.1)
    soup = bf(r.text,"html.parser")
    row = soup.find("table",border="1").findAll("tr")
    #各個鄉鎮的table,一列一列
    for i in row[2:]:
        data={}
        temp = i.findAll("td")
        data["執行單位"]=temp[1].text.rstrip()
        data["標案名稱"]=temp[2].text.rstrip()
        data["詳細連結"]="http://cmdweb.pcc.gov.tw/pccms/owa/"+temp[2].find("a")["href"].rstrip()
        #gov.append(temp[1].text.rstrip())
        #name.append(temp[2].text.rstrip())
        #nameLink.append("http://cmdweb.pcc.gov.tw/pccms/owa/"+temp[2].find("a")["href"].rstrip())
        data_list.append(data)
    return data_list
def getTableDF(datas):
    #dic = {"執行單位":gov, "標案名稱":name, "詳細連結":nameLink}
    df_engineering = pd.DataFrame(datas)
    return df_engineering

    #df_engineering.to_csv("engineering.csv",encoding="utf_8_sig")