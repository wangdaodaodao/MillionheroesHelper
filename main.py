# -*- coding: UTF-8 -*-

import time

import lxml
import requests
from aip import AipOcr
from bs4 import BeautifulSoup# -*- coding: UTF-8 -*-

import time
import re

import lxml
import requests
from aip import AipOcr
from bs4 import BeautifulSoup
from PIL import Image, ImageGrab

t1 = time.time()

search_url_2 = 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word={keywords}'
search_url_1 = 'https://www.baidu.com/s?wd={keywords}&pn=10&rn=50'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4399.400 QQBrowser/9.7.12777.400'
}

filePath_1 = 'screenshot.png'
filePath_2 = 'cropped_img.png'

# 先获得全屏截图，再根据窗口位置进行裁剪，获得待识别的图片
def jietu():
    im = ImageGrab.grab()
    im.save(filePath_1)
    Image.open(filePath_1)
    img_size = im.size
    w = im.size[0]
    h = im.size[1]
    region = im.crop((40, 200, 290, 420))  # 裁剪的区域(分别是左间距，上间距，左间距+宽，上间距+高)
    region.save(filePath_2)
    print('>>>处理完图片共耗时{:.3f}秒\n'.format(time.time() - t1))


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def shibie():
    # 百度aip
    APP_ID = '*******'
    API_KEY = '***********'
    SECRET_KEY = '*************'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    result = aipOcr.basicGeneral(get_file_content(filePath_2), options)
    # 根据识别结果进行，拼接成题目和选项：
    if len(result.get('words_result')) == 5:
        title = result.get('words_result')[0].get(
            'words') + result.get('words_result')[1].get('words')
        an_1 = result.get('words_result')[2].get('words')
        an_2 = result.get('words_result')[3].get('words')
        an_3 = result.get('words_result')[4].get('words')
    elif len(result.get('words_result')) == 6:
        title = result.get('words_result')[0].get('words') + result.get('words_result')[
            1].get('words') + result.get('words_result')[2].get('words')
        an_1 = result.get('words_result')[3].get('words')
        an_2 = result.get('words_result')[4].get('words')
        an_3 = result.get('words_result')[5].get('words')
    elif len(result.get('words_result')) == 4:
        title = result.get('words_result')[0].get('words')
        an_1 = result.get('words_result')[1].get('words')
        an_2 = result.get('words_result')[2].get('words')
        an_3 = result.get('words_result')[3].get('words')
    else:
        title = '^^^遗憾告诉您出错啦，原因可能是：'
        an_1 = '屏幕上未出现题目和选项；'
        an_2 = '选项中出现了数字或公式等非中文字符；'
        an_3 = '题目超过了3行或者是其他某种原因；'
    print(title if '出错' in title else '题目：{}'.format(title.split('.')[-1]))
    print(' A:' + an_1, '\n', 'B:' + an_2, '\n', 'C:' + an_3 , '\n' )

    work = {
        'title': title,
        'A': an_1,
        'B': an_2,
        'C': an_3
    }
    return work


def tishi(title):
    if '没有' in title:
        print('***此道题中含有"没有"， 选择^较少^的选项')
    elif '不' in title:
        print('***此道题中含有"不"， 选择^较少^的选项')
    elif '未' in title:
        print('***此道题中含有"未"， 选择^较少^的选项')
    elif '以下' in title:
        print('***注意，题中可能有"比较"含义，注意分辨答案')
    else:
        print('***建议选择^较多^的选项')


def search_1(work):

    url = search_url_1.format(keywords=work.get('title'))
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    answer = [x.text for x in soup.select('.c-abstract')]
    
    counts = {'an_1': 0, 'an_2': 0, 'an_3': 0}
    for a in answer:        
        if work.get('A') in a:
            counts['an_1'] += 1
        elif work.get('B') in a:
            counts['an_2'] += 1
        elif work.get('C') in a:
            counts['an_3'] += 1
    tips = 'A:出现次数为{}，B:出现次数为{}，C:出现次数为{}'.format(
        counts['an_1'], counts['an_2'], counts['an_3'])
    print(tips)


def search_2(work):
    counts = []
    for tt in [work.get('A'), work.get('B'), work.get('C')]:
        url = search_url_2.format(keywords=work.get('title') + tt)
        # print(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        answer = soup.select('.nums')[0]
        counts.append(answer.text)
    result = 'A:{},B:{},C:{}    --时政娱乐类题目考虑这个选项！'.format(counts[0], counts[1], counts[2])
    print(result)


    
jietu()
try:
    work = shibie()
    if '出错' not in work.get('title'):
        tishi(work.get('title'))   
        search_1(work)
        search_2(work)
except:
    print('!!!请在屏幕上出现题目和选项时运行程序!')

print('\n>>>运行程序全部耗时{:.3f}秒'.format(time.time() - t1))

from PIL import Image, ImageGrab

t1 = time.time()

search_url_2 = 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word={keywords}'
search_url_1 = 'https://www.baidu.com/s?wd={keywords}&pn=10&rn=50'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4399.400 QQBrowser/9.7.12777.400'
}

filePath_1 = 'screenshot.png'
filePath_2 = 'cropped_img.png'

# 先获得全屏截图，再根据窗口位置进行裁剪，获得待识别的图片
def jietu():
    im = ImageGrab.grab()
    im.save(filePath_1)
    Image.open(filePath_1)
    img_size = im.size
    w = im.size[0]
    h = im.size[1]
    region = im.crop((40, 170, 270, 400))  # 裁剪的区域(分别是左间距，上间距，左间距+宽，上间距+高)
    region.save(filePath_2)
    print('>>>处理完图片共耗时{:.3f}秒\n'.format(time.time() - t1))


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def shibie():
    # 百度aip
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    result = aipOcr.basicGeneral(get_file_content(filePath_2), options)
    # 根据识别结果进行，拼接成题目等：
    if len(result.get('words_result')) == 5:
        title = result.get('words_result')[0].get(
            'words') + result.get('words_result')[1].get('words')
        an_1 = result.get('words_result')[2].get('words')
        an_2 = result.get('words_result')[3].get('words')
        an_3 = result.get('words_result')[4].get('words')
    elif len(result.get('words_result')) == 6:
        title = result.get('words_result')[0].get('words') + result.get('words_result')[
            1].get('words') + result.get('words_result')[2].get('words')
        an_1 = result.get('words_result')[3].get('words')
        an_2 = result.get('words_result')[4].get('words')
        an_3 = result.get('words_result')[5].get('words')
    elif len(result.get('words_result')) == 4:
        title = result.get('words_result')[0].get('words')
        an_1 = result.get('words_result')[1].get('words')
        an_2 = result.get('words_result')[2].get('words')
        an_3 = result.get('words_result')[3].get('words')
    else:
        title = '^^^遗憾告诉您出错啦，原因可能是：'
        an_1 = '屏幕上还未出现题目和选项；'
        an_2 = '选项中出现了数字或者公式等；'
        an_3 = '题目超过了3行或者是其他某种原因；'
    print(title if '出错' in title else '题目：{}'.format(title.split('.')[-1]))
    print(' A:' + an_1, '\n', 'B:' + an_2, '\n', 'C:' + an_3 , '\n' )

    work = {
        'title': title,
        'A': an_1,
        'B': an_2,
        'C': an_3
    }
    return work


def tishi(title):
    if '出错' not in title:
        if '没有' in title:
            print('***此道题中含有"没有"， 选择^较少^的选项***')
        elif '不' in title:
            print('***此道题中含有"不"， 选择^较少^的选项***')
        elif '未' in title:
            print('***此道题中含有"未"， 选择^较少^的选项***')
        elif '以下' in title:
            print('***注意，题中可能有"比较"含义，注意分辨答案***')
        else:
            print('***正常题目，选择^较多^的选项***')
    else:
        pass


def search_1(work):
    if '出错' in work.get('title'):
        pass
    else:
        url = search_url_1.format(keywords=work.get('title'))
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        answer = [x.text for x in soup.select('.c-abstract')]
        tt = {'an_1': 0, 'an_2': 0, 'an_3': 0}
        for a in answer:
            if work.get('A') in a:
                tt['an_1'] += 1
            elif work.get('B') in a:
                tt['an_2'] += 1
            elif work.get('C') in a:
                tt['an_3'] += 1
        tips = 'A:出现次数为{}，B:出现次数为{}，C:出现次数为{}'.format(
            tt['an_1'], tt['an_2'], tt['an_3'])
        print(tips)


def search_2(work):
    r = []
    if '出错' in work.get('title'):
        pass
    else:
        for tt in [work.get('A'), work.get('B'), work.get('C')]:
            url = search_url_2.format(keywords=work.get('title') + tt)
            # print(url)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            answer = soup.select('.nums')[0]
            r.append(answer.text)
        result = 'A:{},B:{},C:{}    --时政娱乐类题目考虑这个选项！'.format(r[0], r[1], r[2])
        print(result)


jietu()

try:
    work = shibie()
    tishi(work.get('title'))   
    search_1(work)
    search_2(work)
except:
    print('!!!请在屏幕上出现题目和选项时运行程序!')

print('\n>>>运行程序全部耗时{:.3f}秒'.format(time.time() - t1))
