import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import os,re,json

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
cookietmp = "ARK_ID=JSf336715111f726bbc03b4a26981d7245f336; _atrk_siteuid=N0BNLDqQWonEm54o; _mwa_uniCampaignInfo=1615176896792196943.1615176896792; _ga=GA1.3.109284524.1615176897; _fbp=fb.3.1615176896754.1787100007; __auc=a54a2392178100b9273d7454cac; appier_utmz=%7B%22csr%22%3A%22localhost%253A8888%22%2C%22timestamp%22%3A1615176897%2C%22lcsr%22%3A%22localhost%253A8888%22%7D; _tam=F_cBXygHU-0ZlQzuhpeby_kQ; GoodsBrowsingHistory=6784144_1615199654/; JSESSIONID=E32235667119F7EB9B0B00FF4ED13743-m1.c1-shop17; DCODE=1114701531; wshop=wshop_web_c_17; bid=effbc83f49cde7a12004594861343ff4; isBI=1; _mwa_uniVisitorInfo=1615176896789881900.1615176896789.3.1615276394264; __asc=7c9d04cd17815f9c75b2472b2d6; _gid=GA1.3.1100377939.1615276394; _atrk_ssid=OA9gWRLFm1vIfxcu-7OnYn; _gat_gtag_UA_22652017_1=1; l_code=1114700000; FTOOTH=11; _atrk_sessidx=6; appier_pv_counterERlDyPL9yO7gfOb=2; appier_page_isView_ERlDyPL9yO7gfOb=d222fcf94ecd5072fd0f1ae419614d00e4c0cda48f80bce0a5dadf95cf14eb48; _mwa_uniSessionInfo=1615276394262945168.1615276394262.5.1615276599752; cto_bundle=JbWwnV92eGx1V01SMiUyRmVVck1ja0JPOHNtSHhsOGh3YktaMTY1R3ZEZkduOSUyRkZGeFRTNDhkWFpEajdwWkxMamRCTnB1U2VIUnRXNW1vSzcwNk1ZbVloZ3ZRRG5kUm5kNFQlMkJqMkpITDZiSUw4UmRNUHg1eWZBeVNyS3hpZTR4RVF2dFJwS0pZeHZKTjVkMFZMT0NEUDMwJTJCSjd4dyUzRCUzRA"
cookies = {}
for i in cookietmp.split(";"):
    cookies[i.split("=")[0].lstrip()] = i.split("=")[1]

momo = r"./momo"
if not os.path.exists(momo):
    os.mkdir(momo)

def find_total_page(words):   # 找出最後一頁以及判斷翻頁的網址規則
    if re.search('(.*)p_orderType\=(.*)',words):
        url_ls = words + '&showType=chessboardType&p_pageNum={}'
    elif re.search('(.*)flag=L(.*)',words):
        url_ls = words.split('&',1)[0] + '&pageNum={}'+ '&' + words.split('&',1)[1]
    else:
        url_ls = words + '&p_orderType=6&showType=chessboardType&p_pageNum={}'
    driver.get(words)
    page = driver.page_source
    soup_ls = BeautifulSoup(page, "lxml")
    try:
        lastpage = int(soup_ls.select('div[class="pageArea"] dt')[0].text.split('/')[1])
    except :
        lastpage = 1
    return url_ls,lastpage

url = 'https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1199900000&mdiv=1099700000-bt_0_957_01-&ctype=B' #美妝個清
res = requests.get(url, headers = headers, cookies = cookies)
soup = BeautifulSoup(res.text,"lxml")
board = []
for i in soup.select('div[class="contenttop topArea"] ')[2].select('li'):
    board.append(i.a['href'])
    for k in board :    #上列標題的所有內容    #####品牌旗艦店的都先跳過######
        res1 = requests.get(k, headers=headers, cookies=cookies)
        soup1 = BeautifulSoup(res1.text, "lxml")
        left = []
        for u in soup1.select('[class="BTDME BTDMS 1114700000"] a'):
            if u.text == '更多':
                pass
            elif u['href'].startswith('http') == False:
                left.append({u.text: 'https://www.momoshop.com.tw' + u['href']})
            else:
                left.append({u.text: u['href']})
        for l in left:
            for n in l.values():
                output = []
                # 各商品內容
                lastpage = find_total_page(n)
                print(lastpage[0],'共'+str(lastpage[1])+'頁')
                for j in range(lastpage[1]): #翻頁
                    print([x for x in l.keys()][0],"第{}頁".format(j+1))
                    driver.implicitly_wait(10)
                    driver = Chrome('./chromedriver')
                    url3 = lastpage[0].format(j+1)
                    print(url3)
                    driver.get(url3)
                    page = driver.page_source
                    soup2 = BeautifulSoup(page, "lxml")
                    for m in soup2.select('div[class="prdListArea bt770class"] li'):    #soup2.select('div[class="prdListArea bt770class"] a[class="prdUrl"]')
                        #進到各商品的頁面
                        obj = {}
                        url4 = 'https://www.momoshop.com.tw' + m.find_all('a', href=True)[0]['href']
                        res4 = requests.get(url4, headers=headers, cookies=cookies)
                        soup4 = BeautifulSoup(res4.text, "lxml")
                        obj['web'] = 'momo'
                        obj['board'] = soup.select('[id="toothUl"] li')[2].text    #[2]是位子，上方欄位有11個
                        obj['tag'] = i.a.text
                        try:
                            obj['desc'] = m.h3.text
                        except:
                            obj['desc'] = m.a['title']
                        try:
                            for o in soup4.select('div[class = "vendordetailview specification"] tr'):
                                obj[o.th.text] = o.td.text  #框框裡所有內容
                        except :
                            pass
                        small = []
                        for z in soup4.select('div[class="vendordetailview related_category"] a'):
                            small.append(z.text.strip())
                        obj['小分類參考依據'] = list(set(small))
                        obj['url'] = url4
                        output.append(obj)
                        # print(obj)
                print(output)
                print(len(output))
                with open(momo + "/" + "{}".format(i.a.text) + "/" + "{}_{}".format(i.a.text,[x for x in l.keys()][0]) + ".json", "w",encoding="utf-8") as f:
                    json.dump(output, f, ensure_ascii=False, indent=2)

                driver.close()