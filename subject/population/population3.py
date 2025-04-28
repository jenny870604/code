import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

# 網址+年份
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

# 自訂排序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 提取市縣的函數
def extract_city(site_id):
    if '縣' in site_id:
        return site_id.split('縣')[0] + '縣'
    elif '市' in site_id:
        return site_id.split('市')[0] + '市'
    else:
        return site_id

# 儲存資料
data = {}

for url, year in url_years:
    response = requests.get(url)
    result = response.json()
    records = result['result']['records']
    
    # 轉成DataFrame
    df = pd.DataFrame(records)
    
    # 保留 site_id 中有「市」或「縣」且長度 <=8
    df = df[df['site_id'].str.contains('市|縣') & (df['site_id'].str.len() <= 8)]
    
    # 提取市/縣
    df['city'] = df['site_id'].apply(extract_city)
    
    # 特別處理：2012~2014 的「桃園縣」改成「桃園市」
    if year <= 2014:
        df['city'] = df['city'].replace('桃園縣', '桃園市')

    # 把每個縣市的人口數記錄下來
    for _, row in df.iterrows():
        city = row['city']
        total_pop = int(row['people_total'])  # 去掉千分位逗號

        if city not in data:
            data[city] = {}
        # 累加這一年的總人口
        if year in data[city]:
            data[city][year] += total_pop
        else:
            data[city][year] = total_pop

        # if city not in data:
        #     data[city] = {}
        # data[city][year] = total_pop

# 整理成DataFrame
final_df = pd.DataFrame.from_dict(data, orient='index')
final_df = final_df.reindex(custom_order)  # 按自訂順序排縣市
final_df = final_df.sort_index(axis=1)     # 年份升冪排序

print(final_df)

# 可以選擇存檔
# final_df.to_csv('population_by_county.csv', encoding='utf-8-sig')
# final_df.to_excel('population_by_county.xlsx')

# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
fontManager.addfont("ChineseFont.ttf") #加入字體
mlp.rc("font",family="ChineseFont") #設定使用這個字體

# 設定樣式
# sns.set(style="whitegrid")

# 畫圖：每個縣市的歷年人口變化
plt.figure(figsize=(12, 8))

# 設定顏色區間，顏色會與年份對應
colors = sns.color_palette("coolwarm", n_colors=len(final_df.columns))

# 繪製每個縣市的折線圖
# for city, row in final_df.iterrows():
#     plt.plot(final_df.columns, row, label=city, marker='o')
# 繪製每個縣市的折線圖
lines = []  # 存每條線條，之後設定cursor
for city, row in final_df.iterrows():
    line, = plt.plot(final_df.columns, row, label=city, marker='o')
    lines.append(line)

# 添加標題和標籤
plt.title('歷年各縣市人口變化', fontsize=16)
plt.xlabel('年份', fontsize=12)
plt.ylabel('總人口數', fontsize=12)
plt.xticks(rotation=45)

# 顯示圖例
plt.legend(title='縣市', bbox_to_anchor=(1.05, 1), loc='upper left')

# 加上互動游標
cursor = mplcursors.cursor(lines, hover=True)

@cursor.connect("add")
def on_add(sel):
    line = sel.artist
    city = line.get_label()
    x, y = sel.target
    sel.annotation.set(text=f"{city}\n年份: {int(x)}\n人口: {int(y):,}")  # 加上千分位


# 顯示圖形
plt.tight_layout()
plt.show()