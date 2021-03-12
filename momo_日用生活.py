import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import os,re,json

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
cookietmp = "ARK_ID=JSf336715111f726bbc03b4a26981d7245f336; _atrk_siteuid=N0BNLDqQWonEm54o; _mwa_uniCampaignInfo=1615176896792196943.1615176896792; _ga=GA1.3.109284524.1615176897; _fbp=fb.3.1615176896754.1787100007; __auc=a54a2392178100b9273d7454cac; appier_utmz=%7B%22csr%22%3A%22localhost%253A8888%22%2C%22timestamp%22%3A1615176897%2C%22lcsr%22%3A%22localhost%253A8888%22%7D; _tam=F_cBXygHU-0ZlQzuhpeby_kQ; _gid=GA1.3.1100377939.1615276394; firstTimeOpenShop=forever; bid=3dd6ec9228ea8ff7ca994d29ffa4b0a0; isBI=1; TN=undefined; CN=undefined; CM=undefined; wshop=wshop_web_b_35; DCODE=1114701689; GoodsBrowsingHistory=7631929_1615226377/8596950_1615217020/7947841_1615457886/6855167_1615054126; l_code=3999900000; FTOOTH=39; JSESSIONID=277FA1561A2B3E204FF507A457F66AC0-m1.b1-shop35; _mwa_uniVisitorInfo=1615176896789881900.1615176896789.20.1615537526396; __asc=98c50cba178258a568edc100403; _gat_gtag_UA_22652017_1=1; _atrk_ssid=32B5I6toB6uVqp_ZhXnqgI; _atrk_sessidx=2; appier_pv_counterERlDyPL9yO7gfOb=76; appier_page_isView_ERlDyPL9yO7gfOb=d222fcf94ecd5072fd0f1ae419614d00e4c0cda48f80bce0a5dadf95cf14eb48; _mwa_uniSessionInfo=1615537526395546013.1615537526395.2.1615537526948; cto_bundle=nPE1q192eGx1V01SMiUyRmVVck1ja0JPOHNtSDQ4OTcxU1JyelBicjk2MzFNbzhTSyUyQlEyYnQwek5sZEtoWjMyb0FHNE1WbTREcVNsM1lucUcwZFEwZHB1MHFRYlplbzdZZUMwNmNtYmZ3dFpscSUyRk8xamo2ZXEySGtmTlB6c1V1MUgyaHpwU3dONjQ1ZkJGc3diRFQxUW9IUzhIblElM0QlM0Q"
cookies = {}
for i in cookietmp.split(";"):
    cookies[i.split("=")[0].lstrip()] = i.split("=")[1]

momo = r"./momo/日用生活"
if not os.path.exists(momo):
    os.mkdir(momo)

def categ(o): #判別左邊標籤是否包含"/"
    if '/' in o:
        dog = o.replace('/','-')
    else:
        dog = o
    return dog

def find_total_page(words):   # 找出最後一頁以及判斷翻頁的網址規則
    if re.search('(.*)p_orderType\=(.*)',words):
        url_ls = words + '&showType=chessboardType&p_pageNum={}'
    elif re.search('(.*)flag=L(.*)',words):
        url_ls = words.split('&',1)[0] + '&pageNum={}'+ '&' + words.split('&',1)[1]
    else:
        url_ls = words + '&p_orderType=6&showType=chessboardType&p_pageNum={}'
    driver = Chrome('./chromedriver')
    driver.get(words)
    page = driver.page_source
    soup_ls = BeautifulSoup(page, "lxml")
    try:
        lastpage = int(soup_ls.select('div[class="pageArea"] dt')[0].text.split('/')[1])
    except :
        lastpage = 1
    driver.close()
    return url_ls,lastpage

url = 'https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1199900000&mdiv=1099700000-bt_0_957_01-&ctype=B' #美妝個清
res = requests.get(url, headers = headers, cookies = cookies)
soup = BeautifulSoup(res.text,"lxml")

for k in soup.select('div[class="contenttop topArea"] ')[9].select('li') :    #上列標題的所有內容    #####品牌旗艦店的都先跳過######
    res1 = requests.get(k.a['href'], headers=headers, cookies=cookies)
    soup1 = BeautifulSoup(res1.text, "lxml")
    left = []
    for u in soup1.select('div[id="bt_category_Content"] a'):
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
                driver = Chrome('./chromedriver')
                driver.implicitly_wait(15)
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
                    obj['board'] = soup.select('[id="toothUl"] li')[9].text    #[2]是位子，上方欄位有11個
                    obj['tag'] = k.a.text
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
            momo_sheet = momo+ "/" + "{}".format(k.a.text)
            if not os.path.exists(momo_sheet):
                os.mkdir(momo_sheet)
            with open(momo + "/" + "{}".format(k.a.text) + "/" + "{}_{}".format(k.a.text,categ([x for x in l.keys()][0].lstrip().rstrip())) + ".json", "w",encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            driver.close()