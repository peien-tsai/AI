import requests
from bs4 import BeautifulSoup
import json,os

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
cookietmp = "language=zt; user-group=anonymous; anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; _gcl_au=1.1.1400927384.1612346432; gaUserId=7d7094bb-c5d5-4d75-909d-4562344433bf; _fbp=fb.2.1612346431987.843346747; __lt__cid=0e2af073-a846-4591-b4a1-75e2a44ef621; _hjid=9849aeed-8078-4c9e-bce3-bae477b48c57; __BWfp=c1612346433860x4e018f843; _atrk_siteuid=vzJlVBCj0GbyU9DT; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1613641022%2C%22lcsr%22%3A%22google%22%7D; _gaexp=GAX1.3.BpSfE5jqTxyTxBW-QxVfYw.18771.1; JSESSIONID=BD5795C773C957017AE37B5C0D2D8EFC.twpfa37n; comingFromCookie=null; _gid=GA1.3.1630197074.1614664793; showPopupOnMyBacketPage=null; _hjIncludedInPageviewSample=1; _hjTLDTest=1; _hjIncludedInSessionSample=1; _TUCI_T=sessionNumber+18688&pageView+18688; Tagtoo_pta=pta_03+_1007_&gpa+_&gpb+_&gpc+_&vip+_&lta+_; plp-view-history-products=; appier_page_isView_PageView_1ae7=ffa00d4b3a1b553351696a3f9471a703170b7ee6f5a933f7c13ac8d72ed21179; AKA_A2=A; __lt__sid=d899e18b-9f33ec3f; _atrk_ssid=ec2UJohmzRB9BES59zD71a; appier_pv_counterViewTwoPages_5556=0; appier_page_isView_ViewTwoPages_5556=ffa00d4b3a1b553351696a3f9471a703170b7ee6f5a933f7c13ac8d72ed21179; _TUCS=1; ak_bmsc=09C2BF8C1A761094C6D8B6C8EB08D8F1CB4A435D6D380000AD0D3E60F36AD63C~plMWYqQl+046LVCAOmwMyH5z59gIT+RRSaAtutHyHUQz+Ihx7LRSgszbT2gl14+UwZRCxeccImsCW2vuzVOOMCa6JKKVYPXAiriAqICU1hRyWw8h9U53vTWLp/8ytyER8YsskRKl6MrAi/0VWdeMbkFUvYi0Sqc/zJM1F16pxcZC1hjeGJpVKgMmjTtk1cyjp6ey0qGscDHYi/M9pqrbl0yFn+haR7yZbF/JSLKwAXoZM=; _ga_5K9BFKFT9K=GS1.1.1614664793.13.1.1614680165.59; _ga=GA1.3.35559524.1612346432; _dc_gtm_UA-28255033-1=1; _gat_UA-28255033-1=1; appier_pv_counterPageView_1ae7=9; _atrk_sessidx=12; ins-storage-version=190; QueueITAccepted-SDFrts345E-V3_watsonprdtw=EventId%3Dwatsonprdtw%26QueueId%3Da7a62b50-f280-436f-a493-895abf55fe40%26RedirectType%3Dsafetynet%26IssueTime%3D1614680166%26Hash%3D1bab1876c16cbf26342eafb97c2c33049060332423dfdea1fa92d1f4e6c291e0; bm_sv=9C7811AFB9A63293D90C6C44AB7A6BD7~tQoRys27d9AX4JTwt1TYX0xtDia8+9YnRQplgf0EOERfGFEGNw+9qjThfTVPwxw8HzWEmxy/PT+w1Y3zWNeqPm91gKzAofgeX8qmDogrL02eKQLl0xn60uXzKin8b5U/qYB6Z3AVNLKjqQA5tyxrbyZ91C3qydCeCPSHjGUb3xI=; _TUCI=sessionNumber+3809&ECId+223&hostname+www.watsons.com.tw&pageView+74965"
cookies = {}
for i in cookietmp.split(";"):
    cookies[i.split("=")[0].lstrip()] = i.split("=")[1]

watsons = r"./watsons"
if not os.path.exists(watsons):
    os.mkdir(watsons)
url = 'https://www.watsons.com.tw/'
res = requests.get(url, headers = headers, cookies = cookies)
soup = BeautifulSoup(res.text,"lxml")
a = soup.select('div[class="navContainer"] a')
move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\r\u3000"))

def categ(o): #判別左邊標籤是否包含"/"
    if '/' in o:
        dog = o.replace('/','-')
    else:
        dog = o
    return dog

for i in a:
    boards = []
    url_boards = 'https://www.watsons.com.tw%s'%(i['href'])
    res_boards = requests.get(url_boards, headers = headers, cookies = cookies)
    soup_boards = BeautifulSoup(res_boards.text,"lxml")
    boards = soup_boards.select('h2[class="h1 threeCategory"] a')
    for j in boards: #去各版
        url_Category = 'https://www.watsons.com.tw'+ j['href']
        print(url_Category)
        res_Category = requests.get(url_Category, headers=headers, cookies=cookies)
        soup_Category = BeautifulSoup(res_Category.text, "lxml")
        try:
            lastpage = int(soup_Category.select('div[class="my-pagination"] a')[-2]['data-page'])
        except IndexError:
            lastpage = 1
        print(lastpage)
        for k in range(lastpage): #翻頁
            output = []
            print("第{}頁".format(k))
            url_Category_page = url_Category + '?q=%3AigcBestSeller&page={}&resultsForPage=32&text=&sort=igcBestSeller&deliveryType='.format(k)
            print(url_Category_page)
            res_Category_page = requests.get(url_Category_page, headers=headers, cookies=cookies)
            soup_Category_page = BeautifulSoup(res_Category_page.text, "lxml")
            Category = soup_Category_page.select('div[class="productItemContainer"]')
            # print(Category)
            for m in Category: #各商品
                obj = {}
                obj['board'] = i.text.lstrip().rstrip()
                obj['category'] = j.text.lstrip().rstrip().split('(')[0].replace("\n",'')
                obj['desc'] = m.select('h3')[0].text.split('\xa0')[1]
                obj['品牌'] = m.select('h3')[0].text.split('\xa0')[0].translate(move)
                obj['url'] = 'https://www.watsons.com.tw' + m.select('a')[0]['href']
                output.append(obj)
                # print(obj)
            print(output)
            with open(watsons + "/" + "{}_{}_第{}頁".format(i.text.lstrip().rstrip(),categ(j.text.lstrip().rstrip().split('(')[0].replace("\n",'')),k) + ".json", "w",encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)






            #以下為該商品頁面抓取資料
            # Category = set(soup_Category_page.select('div[class="bottomProductSales"] a[class="ClickSearchResultEvent_Class gtmAlink"]'))
            # cat_list = []
            # for l in Category:
            #     cat_list.append(l['href'])
            # cat_list = set(cat_list)
            # for m in cat_list: #各商品
            #     obj = {}
            #     url_good = 'https://www.watsons.com.tw' + m  # obj['url'] = url_good
            #     print(url_good)
            #     res_good = requests.get(url_good, headers=headers, cookies=cookies)
            #     soup_good = BeautifulSoup(res_good.text, "lxml")
            #     soup_good.select('table[class="ecTable"]')
            #     obj['board'] = i.text.lstrip().rstrip()
            #     obj['category'] = j.text.lstrip().rstrip().split('(')[0].replace("\n",'')
            #     obj['desc'] = soup_good.select('div[class="PDPImgInfo"] h1')[0].text
            #     obj['品牌'] = soup_good.select('div[class="PDPImgInfo"] a')[0].text.lstrip().rstrip()
            #     obj['url'] = url_good
            #     output.append(obj)
            #     # print(obj)
            # save_data_js = json.dumps(output, ensure_ascii=False)
            # print(output)
            # with open(watsons + "/" + "{}_{}_第{}頁".format(i.text.lstrip().rstrip(),j.text.lstrip().rstrip().split('(')[0].replace("\n",''),k) + ".json", "w",encoding="utf-8") as f:
            #     json.dump(output, f, ensure_ascii=False, indent=2)

