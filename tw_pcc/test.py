import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
import time
import numpy as np

more = pd.read_csv("20191002_09-51-09_engineering.csv")
middle = pd.read_csv("20191002_10-41-33_engineering.csv")
less = pd.read_csv("20191002_11-39-17_engineering.csv")

more = more.append(middle)
more = more.append(middle)
result = more.drop_duplicates(subset=['執行單位','標案名稱','詳細連結'],keep=False)
print(len(result["執行單位"]))
        