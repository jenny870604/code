import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors
from tqdm import tqdm

# 年度網址與年份配對
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

# 自訂縣市排序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 擷取縣市名稱
def extract_city(site_id):
    if '縣' in site_id:
        return site_id.split('縣')[0] + '縣'
    elif '市' in site_id:
        return site_id.split('市')[0] + '市'
    else:
        return site_id

# 儲存每年每縣市人口數的字典
data = {}

# 資料處理主流程
for url, year in tqdm(url_years, desc="處理各年度人口資料"):
    response = requests.get(url, timeout=10)
    result = response.json()
    df = pd.DataFrame(result['result']['records'])

    # 篩選合法資料（site_id 包含「縣」或「市」，且長度不超過 8）
    df = df[df['site_id'].str.contains('市|縣') & (df['site_id'].str.len() <= 8)]

    # 擷取城市
    df['city'] = df['site_id'].apply(extract_city)

    # 特殊情況：桃園縣 → 桃園市
    if year <= 2014:
        df['city'] = df['city'].replace('桃園縣', '桃園市')

    # 將人口欄位轉為數字
    df['people_total'] = pd.to_numeric(df['people_total'], errors='coerce')

    # 用 groupby 直接加總每個縣市該年的人口數
    city_population = df.groupby('city')['people_total'].sum()

    for city, total_pop in city_population.items():
        if city not in data:
            data[city] = {}
        data[city][year] = total_pop

# 整理成 DataFrame
final_df = pd.DataFrame.from_dict(data, orient='index')
final_df = final_df.reindex(custom_order)   # 按縣市順序
final_df = final_df.sort_index(axis=1)      # 按年份升冪排序
final_df = final_df / 10000  # 單位轉換為萬人
print(final_df)

# 可以選擇存檔
final_df.to_csv('2012-2023各縣市總人口數.csv', encoding='utf-8')

# font 設定（載入中文字體）
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 繪圖
plt.figure(figsize=(12, 8))
colors = sns.color_palette("coolwarm", n_colors=len(final_df.columns))

# 繪圖並儲存每條線條
lines = []
for city, row in final_df.iterrows():
    line, = plt.plot(final_df.columns, row, label=city, marker='o')
    lines.append(line)

# 圖表標題與座標軸
plt.title('歷年各縣市人口變化', fontsize=16)
plt.xlabel('年份', fontsize=12)
plt.ylabel('總人口數（萬人）', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='縣市', bbox_to_anchor=(1.05, 1), loc='upper left')

# 游標互動標註
cursor = mplcursors.cursor(lines, hover=True)

@cursor.connect("add")
def on_add(sel):
    line = sel.artist
    city = line.get_label()
    x, y = sel.target
    sel.annotation.set(text=f"{city}\n年份: {int(x)}\n人口: {int(y):,}（萬）")

# 儲存圖表
plt.savefig('2012-2023各縣市總人口數.png', dpi=300, bbox_inches='tight')
plt.tight_layout()
plt.show()