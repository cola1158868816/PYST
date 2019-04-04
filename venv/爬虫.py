# import requests
# # hd={"User-agent":'123'}
# # r = requests.get("http://www.baidu.com",headers=hd)
# #
# # print(r.request.headers)
# # def getHtmlText(url):
# #     try:
# #         r= requests.get(url,timeout=30)
# #         r.raise_for_status()
# #         r.encoding = r.apparent_encoding
# #         return r.text
# #     except:
# #         return "Someting Wrong!"
# import bs4
# soup = bs4.BeautifulSoup(open('demo.html'),'lxml')
# # #print(soup.prettify)
# # print(soup.title)
# # print(soup.body.a)
# # tag = soup.find_all('a')
# # # print(tag)
# # for string in soup.strings:
# #     print(repr(string))
#爬取生活大爆炸
import requests
from bs4 import BeautifulSoup
import time
def get_html(url):
    try:
        r= requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding ='utf-8'
        return r.text
    except:
        return "Someting Wrong!"
def get_content(url):
    comments = []
    html =get_html(url)
    soup = BeautifulSoup(html,'lxml')
    liTags = soup.find_all('li',attrs={'class':'j_thread_list clearfix'})
    for li in liTags:
        comment={}
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find_all(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + \
                              li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            print('出了点小问题')
    return comments
def Out2File(dict):
    '''
    将爬取到的文件写入到本地
    保存到当前目录的 TTBT.txt文件中。

    '''
    with open('TTBT.txt', 'a+') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

        print('当前页面爬取完成')
def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    #循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('所有的信息都已经保存完毕！')
base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn=50'
# 设置需要爬取的页码数量
deep = 3

if __name__ == '__main__':
    main(base_url, deep)
