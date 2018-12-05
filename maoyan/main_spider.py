import requests
import re
from bs4 import BeautifulSoup
import json
import time


def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3464.0 Safari/537.36'
        }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text    # 此处注意             
    return None

def parse_one_page(html):
    soap = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    items = soap.find_all('dd')
    
    for item in items:
        try:
            index = item.find('i').string
            title = item.find('p',class_='name').string
            image = item.find('img',class_='board-img')['data-src']
            actor = item.find('p',class_='star').string.strip()
            time = item.find('p',class_="releasetime").string
            score1 = item.find('i',class_='integer').string 
            score2 = item.find('i',class_='fraction').string
            score = score1 + score2

            yield {'index':index,'title':title,'image':image,'actor':actor,
                   'time':time,'score':score}              #注意yield用法
        except:
            print('not find')
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8')as f:
        print(type(json.dumps(content)))       
        f.write(json.dumps(content,ensure_ascii=False)+'\n')   #json库的dumps()可以实现字典的序列化，ensure_ascii保证输出结果是中文形式
        #而非Unicode编码

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)  
if __name__=='__main__':
    for i in range(10):
        main(offset = 10*i)
        time.sleep(1)
    
