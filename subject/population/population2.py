import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# API 列表（順便加上年份）
url_years = [
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-079", 2023),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-075", 2022),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-071", 2021),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-067", 2020),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-059", 2019),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-055", 2018),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-052", 2017),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-040", 2016),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-024", 2015),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-036", 2014),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-032", 2013),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-021", 2012),
]

# 提取市縣的函數
def extract_city(site_id):
    if '縣' in site_id:
        return site_id.split('縣')[0] + '縣'
    elif '市' in site_id:
        return site_id.split('市')[0] + '市'
    else:
        return site_id

# 存放所有資料
all_data = []

# 下載每個 API 資料
for url, year in url_years:
    response = requests.get(url)
    data = response.json()
    records = data['result']['records']
    df = pd.DataFrame(records)

    # 只保留 site_id 含有「市」或「縣」且長度 <= 8
    df = df[df['site_id'].str.contains('市|縣') & (df['site_id'].str.len() <= 8)]

    # 抓出市縣名稱
    df['city'] = df['site_id'].apply(extract_city)

    # population 欄位轉成數字
    df['population'] = pd.to_numeric(df['people_total'], errors='coerce')

    # 加上年份欄位
    df['year'] = year

    all_data.append(df)

# 把所有資料合併起來
full_df = pd.concat(all_data, ignore_index=True)

# # 設定中文字型（不然中文會亂碼）
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
fontManager.addfont("ChineseFont.ttf") #加入字體
mlp.rc("font",family="ChineseFont") #設定使用這個字體

# 把每一年分開畫圖
for year, group_df in full_df.groupby('year'):
    # 依城市加總人口
    result = group_df.groupby('city')['population'].sum().reset_index()
    result = result.sort_values(by='population', ascending=False)

    # 畫圖
    # plt.figure(figsize=(12, 8))
    plt.figure(figsize=(8, 5))  # 縮小圖片
    plt.bar(result['city'], result['population'], color='skyblue')
    plt.xticks(rotation=45, ha='right', fontsize=8)  # x 軸城市名稱變小一點
    plt.xlabel('縣市', fontsize=10)  # x 軸標籤字體大小
    plt.ylabel('人口總數', fontsize=10)  # y 軸標籤字體大小
    plt.title(f'{year}年各縣市人口總數', fontsize=12)  # 標題字體大小
    plt.tight_layout()

    # 存成圖片
#     plt.savefig(f'population_{year}.png')
#     plt.close()

# print("全部圖片都存好了！")
# 顯示圖形
plt.show()
