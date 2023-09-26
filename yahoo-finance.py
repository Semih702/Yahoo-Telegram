from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from time import sleep
from datetime import datetime
import telegram_bot
import asyncio

df= pd.read_csv("yahoo-finance-latest-news.csv",index_col=0)
#print(df)
title_set=set(df["title"])

text_class_name1 = "Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(3,57px) LineClamp(3,51px)--sm1024 M(0)"
text_class_name2 = "Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(2,38px) LineClamp(2,34px)--sm1024 M(0)"
type_classes= ["Fz(12px) Fw(b) Tt(c) D(ib) Mb(6px) C($c-fuji-blue-1-a) Mend(9px) Mt(-2px)",
               "Fz(12px) Fw(b) Tt(c) D(ib) Mb(6px) C($c-fuji-blue-3-a) Mend(9px) Mt(-2px)",
               "Fz(12px) Fw(b) Tt(c) D(ib) Mb(6px) C($c-fuji-teal-1-a) Mend(9px) Mt(-2px)",
               "Fz(12px) Fw(b) Tt(c) D(ib) Mb(6px) C($c-fuji-orange-b) Mend(9px) Mt(-2px)",
               "Fz(12px) D(ib) Td(n) C(#959595) Mend(3px) Mb(6px) Mend(0px)!"]

news_lists_name = "js-stream-content Pos(r)"
title_class_name = "js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled"
source_class_name = "C(#959595) Fz(11px) D(ib) Mb(6px)"
ad_class_name = "controller gemini-ad native-ad-item Feedback Pos(r)"
adsul_class_name = "My(0) P(0) Wow(bw) Ov(h)"
url="https://finance.yahoo.com/news/"
header={'USER-AGENT': "Mozilla/5.0"}
"""cookies = {'Connection': 'keep-alive',
                   'Expires': '-1',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                   }"""
#Some random Header 

while True:
    try:
        r=requests.get(url,timeout=5,headers=header)
        source= BeautifulSoup(r.content,features="html.parser")

        latest_news_div=source.find("ul",class_=adsul_class_name)

        latest_news = latest_news_div.findAll("li",class_=news_lists_name,limit=3)
        for new in latest_news:
            if new.find("div",class_=ad_class_name): # If the element we got is ad the code will skip.
                continue
            title = new.find("a",class_=title_class_name).text
            if title in title_set:
                break
            title_set.add(title)
            temp=None
            i=0
            while temp is None:
                temp=new.find("div",class_=type_classes[i])
                i+=1
            type_ = temp.text
            source = new.find("div",class_=source_class_name).text
            temp = new.find("p",class_=text_class_name1)
            if not temp:
                temp=new.find("p",class_=text_class_name2)

            text = temp.text
            message= f"{title}\n\n{text}\n\nsource: {source}\ntype:{type_}" # this was the message that will send to telegram bot
            telegram_bot.no+=1  
            asyncio.run(telegram_bot.send_message(message))

            df.loc[len(df.index)] = [title,type_,source,text,datetime.now()]
            df.iloc[-1:].to_csv("yahoo-finance-latest-news.csv",mode="a",header=False)
    except Exception as e: #Sometimes website gives some error or crash this will refresh the page
        sleep(1)
    
