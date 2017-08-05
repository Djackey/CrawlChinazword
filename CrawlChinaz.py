#!/usr/local/bin/python
#-*-coding:utf-8-*-
# 2015-6-26 DaoXin
import pycurl
import StringIO
import urllib
import urllib2
from random import choice
import re
import sys
import string
from bs4 import BeautifulSoup
import requests
import sys
import csv
import xlrd
import xlwt
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

# useragent 列表，大家可以自行去收集。不过在本例中似乎不需要这个
AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-CN) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; zh-CN) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; zh-CN) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Camino/2.2.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Camino/2.2a1pre",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0.112941",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0",
]


class CrawlZzword:

    def __init__(self):
        self.UserAgent = choice(AGENTS)
        self.payload = [
            "Host: rank.chinaz.com",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding: gzip, deflate",
            "Connection: keep-alive",
            "Upgrade-Insecure-Requests: 1"
            "Referer: http://rank.chinaz.com/?host=www.ershenghuo.com&sortType=0&page=1"
            "Upgrade-Insecure-Requests: 1"
        ]

    def curl(self, url):
        while 1:
            try:
                c = pycurl.Curl()
                c.setopt(pycurl.MAXREDIRS, 5)
                c.setopt(pycurl.REFERER, url)
                c.setopt(pycurl.FOLLOWLOCATION, True)
                c.setopt(pycurl.CONNECTTIMEOUT, 120)
                c.setopt(pycurl.TIMEOUT, 120)
                c.setopt(pycurl.ENCODING, 'gzip,deflate')
                # c.setopt(c.PROXY,ip)       '''若使用代理，则取消本行注释'''
                c.fp = StringIO.StringIO()
                c.setopt(pycurl.URL, url)
                # c.setopt(pycurl.HTTPHEADER, headers)
                c.setopt(pycurl.USERAGENT, self.UserAgent)
                c.setopt(c.WRITEFUNCTION, c.fp.write)
                c.perform()
                # code = c.getinfo(c.HTTP_CODE) 返回状态码
                html = c.fp.getvalue()
                return html
            except Exception, what:
                information = '错误信息：%s' % what
                return str(information)
                continue

    def Chinazgjc(self, url, pages):
        keyword_data = []
        wholeindexinfo_data = []
        includenum_data = []
        chinazdict = {}
        urlzzindex = "http://rank.chinaz.com/?host=%s&st=0&c=&sortType=0&page=%s" % (
            url, pages)
        urlzzindexhtml = self.curl(urlzzindex)
        soup = BeautifulSoup(urlzzindexhtml, "lxml")
        keywordulhtml = soup.select(
            ".ResultListWrap .bor-b1s")
        keywordpagehtml = soup.select(".ToolPage-right span")[0]
        keywordpage = re.findall(r"共(\d+)页", urlzzindexhtml)[0]

        for keywordul in keywordulhtml:
            keywordinfohtml = keywordul.select("div:nth-of-type(1) .ellipsis")
            wholeindexinfohtml = keywordul.select("div:nth-of-type(3) a")
            includenumhtml = keywordul.select(".bor-r1s05 a")
            for wholeindexinfo in wholeindexinfohtml:
                wholeindexinfo_data.append(wholeindexinfo.string)
            for includenum in includenumhtml:
                includenum_data.append(includenum.string)
            for keywordinfo in keywordinfohtml:
                keyword_data.append(keywordinfo.string)
        chinazdict = {'keyword': keyword_data,
                      'includenum': includenum_data, 'wholeindex': wholeindexinfo_data, 'keywordpage': keywordpage}
        return chinazdict

# gjcweb = "www.ershenghuo.com"
# crawlzzword = CrawlZzword()
# print crawlzzword.Chinazgjc(gjcweb, 1)
gjcweb = "www.1688.com"
gjcwebxls = gjcweb.replace('.', '')
crawlzzword = CrawlZzword()
pagenum = crawlzzword.Chinazgjc(gjcweb, 1)['keywordpage']
keywordlistzz = []
includenumlistzz = []
wholeindexlistzz = []

for num in range(1, string.atoi(pagenum) + 1):
    keywordlist = crawlzzword.Chinazgjc(gjcweb, num)[
        'keyword']
    print keywordlist
    keywordlistzz.extend(keywordlist)
    includenumlist = crawlzzword.Chinazgjc(
        gjcweb, num)['includenum']
    includenumlistzz.extend(includenumlist)
    wholeindexlist = crawlzzword.Chinazgjc(
        gjcweb, num)['wholeindex']
    wholeindexlistzz.extend(wholeindexlist)


# 创建工作簿
f = xlwt.Workbook()
# 创建一个 user_info 的 sheet
sheet1 = f.add_sheet(u'keyword_info', cell_overwrite_ok=True)

for i in xrange(len(keywordlistzz)):
    sheet1.write(i, 0, keywordlistzz[i])
    sheet1.write(i, 1, includenumlistzz[i])
    sheet1.write(i, 2, wholeindexlistzz[i])

f.save(gjcwebxls + ".xls")
