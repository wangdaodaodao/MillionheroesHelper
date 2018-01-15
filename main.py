# -*- coding: UTF-8 -*-

import requests
import lxml
import time
from bs4 import BeautifulSoup
from aip import AipOcr
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
    region = im.crop((40, 160, 260, 390))  # 裁剪的区域(分别是左间距，上间距，左间距+宽，上间距+高)
    region.save(filePath_2)
    print('>>>处理完图片共耗时{:.3f}秒'.format(time.time() - t1))


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def shibie():
    # 百度aip
    APP_ID = '****'
    API_KEY = '*************'
    SECRET_KEY = '*****************'
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
        title = '遗憾告诉您出错啦，原因可能是：'
        an_1 = '1.屏幕上还未出现题目和选项；'
        an_2 = '2.选项中出现了数字和公式等；'
        an_3 = '3.题目超过了3行或者是其他某种原因；'
    print(title[2:])
    print('A:' + an_1, '\n', 'B:' + an_2, '\n', 'C:' + an_3, '\n', )
    work = {
        'title': title,
        'A': an_1,
        'B': an_2,
        'C': an_3
    }
    return work


def tishi(title):
    if '没有' in title:
        print('***此道题中含有"没有"， 所以注意选择^相反^的选项')
    elif '不' in title:
        print('***此道题中含有"不"， 所以注意选择^相反^的选项')
    elif '以下' in title:
        print('注意，题中可能有“比较”含义，注意分辨搜索答案！')


def search_1(work):
    tishi(work.get('title'))
    url = search_url_1.format(keywords=work.get('title'))
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    answer = soup.select('.c-abstract')
    answer1 = [x.text for x in answer]
    x = 0
    y = 0
    z = 0
    tt = {'an_1': x, 'an_2': y, 'an_3': z}
    for a in answer1:
        if work.get('A') in a:
            tt['an_1'] += 1
        elif work.get('B') in a:
            tt['an_2'] += 1
        elif work.get('C') in a:
            tt['an_3'] += 1
    tips = 'A出现次数为{}，B出现次数为{}，C出现次数为{}。\n建议你选最大值的选项！'.format(
        tt['an_1'], tt['an_2'], tt['an_3'])
    print(tips)


def search_2(work):
    r = []
    tishi(work.get('title'))
    for tt in [work.get('A'), work.get('B'), work.get('C')]:
        url = search_url_2.format(keywords=work.get('title') + tt)
        # print(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        answer = soup.select('.nums')[0]
        r.append(answer.text)
    result = 'A:{},\nB:{},\nC:{},\n'.format(r[0], r[1], r[2])
    print(result)




jietu()

try:
    work = shibie()
    print('---------下方答来自百度搜索条目：------')
    search_1(work)
    print('----下方答案来自百度新闻搜索（政类型题目参考）----')
    search_2(work)
except:
    print('!!!请在屏幕上出现题目和选项时运行程序!')

print('>>>运行程序全部耗时{:.3f}秒'.format(time.time() - t1))
