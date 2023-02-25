import requests
from lxml import etree
import csv
import pandas as pd
from time import sleep
import glob
import os

# 获取文件列表
def get_files(dir):
    file_list = []
    for file in glob.glob(dir):
        file_list.append(file)
    return file_list  # 返回一个文件名列表

def getPages(url):
    urlList = []
    for i in range(1, 16):
        url_withPage = url + f'/page_{i}'
        urlList.append(url_withPage)
    return urlList


def getComment(url, name, csvFile, orig_url, page):
    header = {
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': '__mta=45340443.1677329496977.1677329496977.1677329496977.1; JSESSIONID=node07hplsqzhuitmv0vg7lo4gm123338377.node0; IJSESSIONID=node07hplsqzhuitmv0vg7lo4gm123338377; iuuid=583CC492D788AE1842D3D82F2B14FF64933D5441CDD4705CF5BCC5EFD745BDA1; latlng=22.094403%2C113.494991%2C1677329468311; ci=108; cityname=%E7%8F%A0%E6%B5%B7; _lxsdk_cuid=18688a091750-0184b1c74d6613-26031951-190140-18688a09176c8; _lxsdk=583CC492D788AE1842D3D82F2B14FF64933D5441CDD4705CF5BCC5EFD745BDA1; uuid=b07adb7aa4bc4f0b8254.1677329469.1.0.0; WEBDFPID=9y3224923z9y534719v7438ux5z83z9881311z9094x979582y971u85-1992689470102-1677329469700MMEEEYUfd79fef3d01d5e9aadc18ccd4d0c95072208; token=AgHHIjX0ZHBAVROrKm0RpzaCayZXTTICI35mmf6PcW-ANOd5DFS4jVG0plS2-w8orEmmqAEdGjkr_QAAAAC9FgAA64qQqhr1TEaAUlXKc1xj_-qSgHgnMoOOPb30oGtrOfKiQa57H8Y2a1HjxBd-8yfT; mt_c_token=AgHHIjX0ZHBAVROrKm0RpzaCayZXTTICI35mmf6PcW-ANOd5DFS4jVG0plS2-w8orEmmqAEdGjkr_QAAAAC9FgAA64qQqhr1TEaAUlXKc1xj_-qSgHgnMoOOPb30oGtrOfKiQa57H8Y2a1HjxBd-8yfT; oops=AgHHIjX0ZHBAVROrKm0RpzaCayZXTTICI35mmf6PcW-ANOd5DFS4jVG0plS2-w8orEmmqAEdGjkr_QAAAAC9FgAA64qQqhr1TEaAUlXKc1xj_-qSgHgnMoOOPb30oGtrOfKiQa57H8Y2a1HjxBd-8yfT; userId=2781739921; u=2781739921; isid=AgHHIjX0ZHBAVROrKm0RpzaCayZXTTICI35mmf6PcW-ANOd5DFS4jVG0plS2-w8orEmmqAEdGjkr_QAAAAC9FgAA64qQqhr1TEaAUlXKc1xj_-qSgHgnMoOOPb30oGtrOfKiQa57H8Y2a1HjxBd-8yfT; logintype=normal; webp=1; i_extend=H__a100173__b1; __utma=74597006.1844764136.1677329497.1677329497.1677329497.1; __utmc=74597006; __utmz=74597006.1677329497.1.1.utmcsr=passport.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=74597006.1.10.1677329497; _lxsdk_s=18688a09176-c19-ec8-6d4%7C%7C7',
        'DNT': '1',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.56'
    }

    response = requests.get(url=url, headers=header)
    print(response.url)
    if response.url == 'https://i.meituan.com/error/404':
        print('404')
        return True
    html = response.text
    root = etree.HTML(html)
    commentList = root.xpath('/html/body/dd')

    for comment in commentList:
        fullStarList = comment.xpath('div/div[1]/div[2]/div[2]/span/img[@class="icn_star star_full"]')
        halfStarList = comment.xpath('div/div[1]/div[2]/div[2]/span/img[@class="icn_star star_half"]')
        rate = len(fullStarList) + len(halfStarList) * 0.5

        content = comment.xpath('div/div[2]/p/text()')
        if len(content) == 0:
            part1 = ''.join(comment.xpath('div/div[2]/div/p/text()'))
            part1 = part1.replace(' ', '')
            part1 = part1.replace('\n', '')

            part2 = ''.join(comment.xpath('div/div[2]/div/p/span/text()'))
            part2 = part2.replace(' ', '')
            part2 = part2.replace('\n', '')

            content = part1 + part2
        else:
            content = ''.join(content)

        if rate == 0 or len(content) == 0:
            continue

        print(rate)
        print(content)

        data_dict = {
            '店铺名': name,
            '评论内容': content,
            '评分': rate,
            '原链接': orig_url,
            '页码': page
        }
        csvFile.writerow(data_dict)


if __name__ == '__main__':
    if os.path.exists('评论.csv'):
        log = pd.read_csv('评论.csv')
        page = log['页码'].iloc[-1]
        print(page)
        orig_url_pre = log['原链接'].iloc[-1]
        print(orig_url_pre)

        with open("评论.csv", mode="a", encoding='utf-8', newline="") as f:
            csvFile = csv.DictWriter(f, fieldnames=['店铺名', '评论内容', '评分', '原链接', '页码'])
            df = pd.read_csv('美食.csv')
            orig_url_index = df.query(f'店铺评论页=="{orig_url_pre}"').index.tolist()[0]

            for i in range(orig_url_index, len(df['店铺评论页'])):
                name = df['店铺名'][i]
                print(name)
                orig_url = df['店铺评论页'][i]
                urlList = getPages(orig_url)
                for j in range(page, len(urlList)):
                    is404 = getComment(urlList[j], name, csvFile, orig_url, j + 1)
                    if is404:
                        break
                    sleep(1)
                page = 0
    else:
        with open("评论.csv", mode="a", encoding='utf-8', newline="") as f:
            csvFile = csv.DictWriter(f, fieldnames=['店铺名', '评论内容', '评分', '原链接', '页码'])
            csvFile.writeheader()  # 写入表头
            df = pd.read_csv('美食.csv')
            for i in range(len(df['店铺评论页'])):
                name = df['店铺名'][i]
                print(name)
                orig_url = df['店铺评论页'][i]
                urlList = getPages(orig_url)
                for j in range(len(urlList)):
                    is404 = getComment(urlList[j], name, csvFile, orig_url, j + 1)
                    if is404:
                        break
                    sleep(1)


