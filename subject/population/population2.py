import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# API 列表（加上年份）
url_years = [
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-079", 2024),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-075", 2023),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-071", 2022),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-067", 2021),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-059", 2020),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-055", 2019),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-052", 2018),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-040", 2017),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-024", 2016),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-036", 2015),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-032", 2014),
    ("https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-021", 2013),
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

# 設定中文字型（避免中文亂碼）
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
fontManager.addfont("ChineseFont.ttf") #加入字體
mlp.rc("font",family="ChineseFont") #設定使用這個字體

# 分年份畫圖
for year, group_df in full_df.groupby('year'):
    # 依城市加總人口
    result = group_df.groupby('city')['population'].sum().reset_index()
    result = result.sort_values(by='population', ascending=False)

    # 設定顏色列表，預設是 skyblue
    colors = ['skyblue'] * len(result)

    # 排名前三名特別標金銀銅色
    if len(result) >= 1:
        colors[0] = 'gold'    # 第一名
    if len(result) >= 2:
        colors[1] = 'silver'  # 第二名
    if len(result) >= 3:
        colors[2] = '#cd7f32' # 第三名，銅色 (手動設定 Hex 色碼)

    # 畫圖
    plt.figure(figsize=(12, 8))
    plt.bar(result['city'], result['population'], color=colors)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('縣市')
    plt.ylabel('人口總數')
    plt.title(f'{year}年各縣市人口總數')
    plt.tight_layout()

    # 存成圖片
    plt.savefig(f'population_{year}.png')
    plt.close()

print("全部加上金銀銅的圖片都存好了！🥇🥈🥉")
plt.show()
