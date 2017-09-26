#-*- coding:utf-8 -*-
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import csv
import hashlib
import MySQLdb
import requests
from bs4 import BeautifulSoup

conn = MySQLdb.connect(host="192.168.80.44", user="root", passwd="ahzx2016", port=3306, charset='utf8',db='lijing')
cur = conn.cursor()
def urlitems(fyurl):
    urlz=[]
    for i in range(len(fyurl)):

        HEADERS = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' #模拟登陆的浏览器
                   }
        # driver=webdriver.Chrome()
        # print driver.get(url)

        # res=requests.get(url)
        res= requests.post(fyurl[i],headers=HEADERS)

        soup=BeautifulSoup(res.text,'html.parser')
        # print soup.prettify()
        # print  soup.select('.STYLE8')

        for news in soup.select('.STYLE8'):
            if re.search(ur'处罚信息公开表',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urlz.append(a)
        # print  urlz

    #行政处罚的格式化具体url,并且通过md5加密后写入csv文件
    urls=[]
    xingzhengchufaurl='http://www.cbrc.gov.cn{}'
    with open('urls.csv','a+') as csvfile:
        writer=csv.writer(csvfile)
        for i in range(len(urlz)):
            #每次循环，把装url字符串的暂时列表清空，实现一行行写入
            temptedlist=[]
            urls.append( xingzhengchufaurl.format(urlz[i]))
            #把进过MD5加密的url字符串追加暂时列表中
            temptedlist.append(hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest())
            #writerow里把字符串当做一个list传入才不会被分隔符隔成一个个字母的
            writer.writerow(temptedlist)
            sql="INSERT INTO yjfj_url (urlhs) VALUES ('%s')"%temptedlist[0]
            print sql
            cur.execute(sql)
    cur.close()
    conn.close()

    print urls
    return urls



def fenye(fenyeurl,n):
    fenyeurls=[]
    for i in range(1,n):
        fenyeurls.append(fenyeurl.format(i))
    return fenyeurls

fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current={}'
urlitems(fenye(fenyeurl,203))


