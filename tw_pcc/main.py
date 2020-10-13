import smallCounty
import table
import metadata
import datetime
import pandas as pd
if __name__ == '__main__':
    
    df_smallCounty = smallCounty.smallCounty("http://cmdweb.pcc.gov.tw/pccms/owa/guesmap.userinn")
    df_smallCounty.to_csv(datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")+"_smallCounty.csv",encoding="utf_8_sig")
    data_list1=[]
    for tableLink,name in zip(df_smallCounty["table連結"],df_smallCounty["鄉鎮"]):
        print(tableLink,name)
        data_list1.extend(table.table(tableLink))
    df_table = table.getTableDF(data_list1)
    df_table.to_csv(datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")+"_engineering.csv",encoding="utf_8_sig")
    #df_table = pd.read_csv("20191002_09-51-09_engineering.csv")
    data_list=[]
    for metadataLink in df_table["詳細連結"]:
        data_list.append(metadata.metadata(metadataLink))

    df_metadata = metadata.getMetadataDF(data_list)
    df_metadata.to_csv(datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")+"_metadata.csv",encoding="utf_8_sig")



