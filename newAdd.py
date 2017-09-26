#-*- coding:utf-8 -*-
import requests
import hashlib
import re
import MySQLdb
#调用hashlib里的md5()生成一个md5 hash对象
# m=hashlib.md5()#如果是对一条字符串进行处理，可以print hashlib.new("md5", "Nobody inspects the spammish repetition").hexdigest()
# #生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理
# m.update('http://www.cbrc.gov.cn/chinese/home/docView/xzcf_12E261D4B6BB4EAC88814F839D7F6984.html')
# #加密后的十六进制结果，二进制结果digest()
# print m.hexdigest()
# #继续调用update方法会在前面加密的基础上更新加密
# m.update('http://www.cbrc.gov.cn/chinese/home/docView/D0952CF472AB443486104FB03E6FE862.html')
# m2= m.hexdigest()
# if m1==m2:
#     print "right"
# else:
#     print "gun!"
#

# def compareUrl():
#     pass

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
    urlshash=[]
    xingzhengchufaurl='http://www.cbrc.gov.cn{}'
    #with open('urls.csv','a+') as csvfile:
        # csvfile.seek(0)
        # m1= csvfile.read()
        # print m1
    #第一次与旧的url作对比,取出数据库中第一个url，与手动给出第一次存入url的第一MD5编码对比，若是真就是第一次，否则不是第一次
    cur.execute("SELECT url FROM urltable LIMIT 0,1")
    m=cur.fetchone()
    #fetchaone返回的是一个tuple
    print type(m[0])
    if m[0]==u'2d6a7169444966a22cb3281b91c4bcf5':##这个字符串根据具体数据库改变
        cur.execute("SELECT url FROM urltable LIMIT 0,1")
        m1=(cur.fetchone())[0]
    else:
        cur.execute("SELECT url FROM urltable  ORDER BY id DESC;")
        m1=(cur.fetchone())[0]

    for i in range(len(urlz)):
       # urls.append( hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest())
    #做对比
       m2=hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest()
       # print m2
       if m1==m2: #csvfile.readline()==hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest():
           print"没有更新"
           break
       else:
           #新增数据的url列表
           urls.append(xingzhengchufaurl.format(urlz[i]))
           urlshash.insert(0,m2)

    for i in range(len(urlshash)):
        cur.execute("INSERT INTO urltable (url) VALUES ('%s')"%urlshash[i])
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
urlitems(fenye(fenyeurl,2))

