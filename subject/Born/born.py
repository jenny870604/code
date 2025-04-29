import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# 自訂縣市順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 讀取資料
df = pd.read_csv('./subject/Born/opendata113b050.csv', encoding='utf-8')

# 新增一欄：對應到 custom_order 中的縣市名稱
def match_city(site_id):
    for city in custom_order:
        if str(site_id).startswith(city):
            return city
    return None

df['縣市'] = df['區域別'].apply(match_city)

# 聚合出生人數
grouped = df.groupby('縣市')['嬰兒出生數'].sum().reindex(custom_order).fillna(0).astype(int)

# 取得前三名
top3 = grouped.sort_values(ascending=False).head(3)
medals = ['🥇 金牌', '🥈 銀牌', '🥉 銅牌']
for medal, (city, count) in zip(medals, top3.items()):
    print(f"{medal}: {city} - {count}人")

# 加入中文字體
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 繪圖
plt.figure(figsize=(12, 6))
colors = ['gold' if city == top3.index[0]
          else 'silver' if city == top3.index[1]
          else 'peru' if city == top3.index[2]
          else 'skyblue' for city in custom_order]

bars = plt.bar(custom_order, grouped.values, color=colors)

plt.xticks(rotation=45, ha='right')
plt.xlabel('縣市')
plt.ylabel('出生人數')
plt.title('各縣市嬰兒出生人數')
plt.tight_layout()
# plt.savefig('Born_trends.png', dpi=300, bbox_inches='tight')
plt.show()