import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
import time
countyLink=[]
smallCountyLink=[]
acrossNameList=[]
acrossLink=[]
countyNameList=[]
smallCountyNameList=[]

def smallCounty(URL):
    r = requests.get(URL)
    soup = bf(r.text,"html.parser")
    mainLink = soup.select("frameset frame")
    mainLink = "http://cmdweb.pcc.gov.tw"+mainLink[0]["src"]  #找iframe網址
    r2 = requests.get(mainLink)
    soup2 = bf(r2.text, "html.parser")
    county = soup2.find("map").select("area")
    #縣市Link
    for i in county:
        countyLink.append("http://cmdweb.pcc.gov.tw/pccms/owa/"+i["href"].rstrip())
    #跨區Link和縣市名稱
    for i in countyLink:
        r3 = requests.get(i)
        soup3 = bf(r3.text,"html.parser")
        acrossNameList.append(soup3.select("font")[1].text[:-6])
        countyNameList.append(soup3.select("font")[1].text[1:3])
        acrossLink.append("http://cmdweb.pcc.gov.tw/pccms/owa/"+soup3.find("a")["href"].rstrip())
    #鄉鎮Link和鄉鎮名稱
    def getSmallCounty(countyURL):
        get_r = requests.get(countyURL)
        get_soup = bf(get_r.text, "html.parser")
        smallCounty = get_soup.select("area")
        if len(smallCounty) != 0:
            for i in smallCounty:
                smallCountyLink.append("http://cmdweb.pcc.gov.tw/pccms/owa/"+ i["href"].rstrip())
                #進入鄉鎮meta data抓鄉鎮名
                get_r2 = requests.get("http://cmdweb.pcc.gov.tw/pccms/owa/"+ i["href"].rstrip())
                get_soup2 = bf(get_r2.text, "html.parser")
                smallCountyNameList.append(get_soup2.find("font", color="red").text)
                
    for i in countyLink:
        getSmallCounty(i)

    #鄉鎮Link產生df
    smallCountyNameList.extend(countyNameList)
    smallCountyLink.extend(acrossLink)
    dic_smallCounty={"鄉鎮":smallCountyNameList,"table連結":smallCountyLink}
    df_smallCounty = pd.DataFrame(dic_smallCounty)
    return df_smallCounty
#df_smallCounty.to_csv("smallCounty.csv",encoding="utf_8_sig")