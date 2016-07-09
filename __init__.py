#encoding=utf-8 
from bs4 import BeautifulSoup
import urllib2
import MySQLdb
from BeautifulSoup import UnicodeDammit
import sys
from douban import get_soup
import re

reload(sys)
sys.setdefaultencoding('utf-8')
conn = MySQLdb.Connect(host='127.0.0.1',user='root',passwd="123456",db='dbdushu',port=3306,charset='utf8')
tag_url = 'https://book.douban.com/tag/'
html_url = 'https://book.douban.com'
request = urllib2.Request(html_url)
response = urllib2.urlopen(request)
getsoup1 = get_soup.SoupGet()
soup1 = getsoup1.soupget(tag_url)
# print soup1.find_all('div','info')
# print response.read()
soup = BeautifulSoup(response,from_encoding="utf8")
# print soup.find_all('a')
# for link in soup.find_all('a'):
#     print (link.get_text())
# imgget = soup.find_all('img')
# for img in imgget:
#     print img.get('class')
#     if img.get('alt') != None:
#         print img.get('alt')
divget = soup.find_all('div',{'class':'cover'})
# file1 = open('test.txt','w')
# file1.write(soup.prettify('utf8'))
# file1.close()
# print soup.original_encoding
atag = soup1.find_all('a','tag')
tag_list = []
i = 0
for tag in atag:
#     print tag['href']
    next_url = html_url+tag['href']
    tag_list.insert(i,next_url)
    booktype = tag['href'][-2:]
#     print new_url
    
    while(1):
        soup1 = getsoup1.soupget(next_url)
        pagebooks = soup1.find_all('li','subject-item')
        cursor = conn.cursor()
        for book in pagebooks:
            name = book.find('div','info').a['title'].strip()
            if book.find('div','info').find('div','pub') is not None:
                info = book.find('div','info').find('div','pub').get_text().strip()
            else:
                info = "暂无信息"
            if book.find('div','info').find('span','rating_nums') is not None:
                commentlevel = book.find('div','info').find('span','rating_nums').get_text()
            else:
                commentlevel = "暂无评价"
            if book.find('div','info').find('span','pl') is not None:
                commentnum = book.find('div','info').find('span','pl').get_text().strip()[1:-1]
            else:
                commentnum = "暂无评论数"
            if book.find('div','info').find('p') is not None:
                introduction = book.find('div','info').find('p').get_text().strip()
            else:
                introduction = "无"
            href = book.find('div','info').a['href']
            imgsrc = book.find('div','pic').img['src']
#             print name,commentlevel,commentnum,info,introduction,href,imgsrc,booktype
            
            cursor.execute("select * from booklist where bookname = %s",(name,))
            if cursor.fetchone() is not None:
                pass
            else:
                insertsql = "insert into booklist (bookname,bookinfo,booktype,introduction,commentnum,commentlevel,imgsrc,href) values ('"\
                + name +"','"+ info +"','"+ booktype +"','"+ introduction +"','"+ commentnum +"','"+ commentlevel +"','"+ imgsrc +"','"\
                + href +"')"
                try:
                    cursor.execute(insertsql)
                    conn.commit()
                except:
                    conn.rollback()
                    file1 = open('rollbackfile','a')
                    file1.write(name+' rollback\n')
                    file1.close()
        try:
            urlget =  soup1.find('span','thispage').find_next('a')['href']
            next_url = html_url+urlget
            if next_url in tag_list:
                break
            tag_list.insert(i,next_url)
#             print tag_list
            print next_url
        except:
            print 'end this tag'
            break
conn.close()
# for book in divget:
#     print book.a['href']
#     bookname = book.a.img['alt'].encode('utf8')
#     print book.a.img['src']
#     print bookname['alt']
#     cursor = conn.cursor()
#     sql = "insert into booklist (bookname,href,imgsrc) values ('" \
#     +bookname+"','"+book.a['href'].encode('utf8')+"','"+book.a.img['src'].encode('utf8')+"')"
#     cursor.execute(sql)
#     conn.commit()
# conn.close()