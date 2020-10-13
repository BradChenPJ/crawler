import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
import time
import numpy as np



def metadata(tableURL):
    data={}
    pd.DataFrame()
    designFlag = True
    r = requests.get(tableURL)
    #content = r.content.decode()
    #html = etree.HTML(content)
    soup = bf(r.text, "lxml")
    table = soup.find("table", border="2").findAll("font")
    print(tableURL)
    #一列裡面的metadata
    for i in range(len(table)):
        try:
            if "工程名稱" in table[i].text:
                data["工程名稱"]=table[i+2].text.strip()
                #engName.append(table[i+2].text.strip())
            elif "設計單位" in table[i].text:
                data["設計單位"]=table[i+2].text.strip()
                #designName.append(table[i+2].text.strip())
                #designFlag = False
            elif "監造單位" in table[i].text:
                data["監造單位"]=table[i+2].text.strip()
                #superviseName.append(table[i+2].text.strip())
            elif "施工廠商" in table[i].text:
                data["施工廠商"]=table[i+2].text.strip()
                #conductName.append(table[i+2].text.strip())
            elif "施工期間" in table[i].text:
                data["施工期間"]=table[i+2].text.strip().replace("\n","")
                # duration.append(table[i+2].text.strip().replace("\n",""))
            elif "決標金額" in table[i].text:
                data["決標金額"]=table[i+1].text.strip()
            elif "重要公告" in table[i].text:
                data["重要公告"]=table[i+2].text.strip().replace("\n","")
                #notice.append(table[i+2].text.strip().replace("\n",""))
        except:
            pass
    
    return data
def getMetadataDF(datas):
    #dic = {"工程名稱":engName,"設計單位":designName,"監造單位":superviseName,"施工廠商":conductName,"施工期間":duration,"重要公告":notice}
    #df_metadata = pd.DataFrame(dic)
    df_metadata = pd.DataFrame(datas)
   
    return df_metadata
