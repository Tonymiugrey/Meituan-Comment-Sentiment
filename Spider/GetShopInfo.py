import csv
import requests
import pandas as pd
# import pprint

def requestData(search, page):
    url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/108?'
    param = {
        'uuid': '841c40d77b6f43aa9302.1669191956.1.0.0',
        'userid': '2781739921',
        'limit': '32', # 一页32个
        'offset': (page-1)*32,
        'cateId': '-1',
        'q': search,
        'token': 'AgEMIQk5cBVCbpQdbdqJoYjAY2l4oNe3TsrI26EOZArtxKcmKkdoaYx2IToaJjEAOR7RZy1Kc1H9tAAAAADUFgAAWx3IGnJK5hcC25_LZIpoDpi9QYZtdwKo-PuiwLQ0menegi33SxLqcBrEivqbHMXH'
    }
    header = {
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': '_lxsdk_cuid=184a346bd40c8-04b0ac911de011-26021e51-125f51-184a346bd40c8; _lxsdk=184a346bd40c8-04b0ac911de011-26021e51-125f51-184a346bd40c8; uuid=841c40d77b6f43aa9302.1669191956.1.0.0; _ga=GA1.1.915482255.1669273723; _ga_95GX0SH5GM=GS1.1.1669903266.3.0.1669903266.0.0.0; _lx_utm=utm_source=Baidu&utm_medium=organic; WEBDFPID=u67y49uuuxxz557z04103135w1u472v181316yzyy1597958u6933601-1992607300924-1677247298686OOKQMAWfd79fef3d01d5e9aadc18ccd4d0c95075988; qruuid=6757816a-b829-4fd6-826a-7cc5f499dbde; token2=AgEMIQk5cBVCbpQdbdqJoYjAY2l4oNe3TsrI26EOZArtxKcmKkdoaYx2IToaJjEAOR7RZy1Kc1H9tAAAAADUFgAAWx3IGnJK5hcC25_LZIpoDpi9QYZtdwKo-PuiwLQ0menegi33SxLqcBrEivqbHMXH; oops=AgEMIQk5cBVCbpQdbdqJoYjAY2l4oNe3TsrI26EOZArtxKcmKkdoaYx2IToaJjEAOR7RZy1Kc1H9tAAAAADUFgAAWx3IGnJK5hcC25_LZIpoDpi9QYZtdwKo-PuiwLQ0menegi33SxLqcBrEivqbHMXH; lt=AgEMIQk5cBVCbpQdbdqJoYjAY2l4oNe3TsrI26EOZArtxKcmKkdoaYx2IToaJjEAOR7RZy1Kc1H9tAAAAADUFgAAWx3IGnJK5hcC25_LZIpoDpi9QYZtdwKo-PuiwLQ0menegi33SxLqcBrEivqbHMXH; u=2781739921; n=Ty.729; unc=Ty.729; _hc.v=73b35f0e-4a02-47bc-1000-287976df2cb0.1677249413; lat=22.237772; lng=113.542263; ci=108; rvct=108,1; firstTime=1677252411251; _lxsdk_s=18683babb4e-0c8-49e-44b||113',
        'DNT': '1',
        "Host": "apimobile.meituan.com",
        'Referer': "https://zh.meituan.com/",
        'Origin': "https://zh.meituan.com",
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    try:
        # 将参数、表头加载后发送请求
        response = requests.get(url=url, params=param, headers=header)
        # 反馈的数据进行json格式解析
        data_json = response.json()
        print("Page {page} Success".format(page=page))
        # pprint.pprint(data_json) # 标准格式打印 使用时需要import pprint
        return data_json
    except Exception as e:
        print("requests请求失败" + str(e))


def parseData(data, csvFile):
    """对得到的json数据进行解析"""
    # 根据此前对数据的分析结果，searchResult值 位于data字典中，是一个列表形式数据
    searchResult = data['data']['searchResult']
    try:
        # 对searchResult列表进行索引解析，其内容是以字典形式存放，我们提取时也以字典存储
        for item in searchResult:
            data_dict = {
                '店铺ID': item['id'],
                '店铺名': item['title'],
                '店铺评论页': f'https://i.meituan.com/poi/{item["id"]}/feedbacks',
                '店铺所在位置': item['areaname'],
                '人均消费': item['avgprice'],
                '评分': item['avgscore'],
                '美食名称': item['backCateName'],
                '店铺图片链接': item['imageUrl'],
                '纬度': item['latitude'],
                '经度': item['longitude'],
                '最低价格': item['lowestprice'],
            }
            # 逐行立刻写入数据，以防出错导致的前功尽弃，同样是依照字典进行
            csvFile.writerow(data_dict)
    except Exception as e:
        print("数据解析失败" + str(e))


if __name__ == '__main__':
    with open("美食.csv", mode="a", encoding='utf-8', newline="") as f:
        csvFile = csv.DictWriter(f, fieldnames=['店铺ID', '店铺名', '店铺评论页', '店铺所在位置', '人均消费', '评分',
                                                  '美食名称', '店铺图片链接', '纬度', '经度', '最低价格'])
        csvFile.writeheader()  # 写入表头
        # 搜索的页数
        for i in range(9):
            parseData(data=requestData(search='美食', page=i), csvFile=csvFile)

    df = pd.read_csv('美食.csv')
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    print(df.shape[0])
    df.to_csv('美食.csv')