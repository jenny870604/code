import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

# 自訂縣市順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 讀取資料
df = pd.read_csv('/Users/wuchiachen/Desktop/code/subject/Born/opendata113b050.csv', encoding='utf-8')

# 累加各縣市的出生人數
birth_counts = defaultdict(int)
for _, row in df.iterrows():
    site_id = row['區域別']
    count = int(row['嬰兒出生數'])
    for city in custom_order:
        if str(site_id).startswith(city):
            birth_counts[city] += count
            break

# 取得前三名（出生人數最多）
top3 = sorted(birth_counts.items(), key=lambda x: x[1], reverse=True)[:3]

# 輸出前三名
medals = ['🥇 金牌', '🥈 銀牌', '🥉 銅牌']
for medal, (city, count) in zip(medals, top3):
    print(f"{medal}: {city} - {count}人")

# 繪製直方圖
cities = custom_order
counts = [birth_counts[city] for city in cities]

fontManager.addfont("ChineseFont.ttf") #加入字體
mlp.rc("font",family="ChineseFont") #設定使用這個字體

plt.figure(figsize=(12, 6))
bars = plt.bar(cities, counts, color='skyblue')

# 標記前三名顏色
for city, bar in zip(cities, bars):
    if city == top3[0][0]:
        bar.set_color('gold')
    elif city == top3[1][0]:
        bar.set_color('silver')
    elif city == top3[2][0]:
        bar.set_color('peru')  # 銅色

plt.xticks(rotation=45, ha='right')
plt.xlabel('縣市')
plt.ylabel('出生人數')
plt.title('各縣市嬰兒出生人數')
plt.savefig('Born_trends.png', dpi=300, bbox_inches='tight')
plt.tight_layout()
plt.show()
