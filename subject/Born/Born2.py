import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

# 自訂縣市順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 年度與檔案對應
files = {
    2015: "./subject/Born/opendata104b050.csv",
    2016: "./subject/Born/opendata105b050.csv",
    2017: "./subject/Born/opendata106b050.csv",
    2018: "./subject/Born/opendata107b050.csv",
    2019: "./subject/Born/opendata108b050.csv",
    2020: "./subject/Born/opendata109b050.csv",
    2021: "./subject/Born/opendata110b050.csv",
    2022: "./subject/Born/opendata111b050.csv",
    2023: "./subject/Born/opendata112b050.csv",
    2024: "./subject/Born/opendata113b050.csv",
}

# 用來提取縣市的方法
def match_city(site_id):
    for city in custom_order:
        if str(site_id).startswith(city):
            return city
    return None

# 儲存每年各縣市出生數的資料
data = pd.DataFrame(index=custom_order)

for year, file_path in files.items():
    df = pd.read_csv(file_path, encoding='utf-8')
    df['縣市'] = df['區域別'].apply(match_city)
    grouped = df.groupby('縣市')['嬰兒出生數'].sum().reindex(custom_order).fillna(0).astype(int)
    data[year] = grouped

# 儲存為 CSV
data.to_csv('2015-2024出生人數.csv', encoding='utf-8')

# 設定中文字體
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 畫圖
plt.figure(figsize=(12, 8))

# 儲存每條線條
lines = []
for city, row in data.iterrows():
    line, = plt.plot(data.columns, row, label=city, marker='o')
    lines.append(line)

plt.xlabel('年度')
plt.ylabel('出生人數')
plt.title('2015-2024 各縣市出生人數變化')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()

# 加上互動游標
cursor = mplcursors.cursor(lines, hover=True)

@cursor.connect("add")
def on_add(sel):
    city = sel.artist.get_label()  # 獲取線條的標籤，即縣市名稱
    y = int(sel.target[1])  # y座標即為出生人數
    sel.annotation.set(text=f"{city}\n出生人數: {y}人")

# 儲存圖檔
plt.savefig('2015-2024出生人數.png', dpi=300, bbox_inches='tight')
plt.show()
