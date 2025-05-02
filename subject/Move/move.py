import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

# 自定義縣市順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 讀取 Excel 中的 '01-12累計' 工作表
file = './subject/Move/縣市遷入及遷出(按登記)-113年.xls'  # <- 檔案名稱
df = pd.read_excel(file, sheet_name='01-12累計', header=None)

# 建立資料字典
total_in = {}
total_out = {}

# 根據你提供的規則：i 從 8 開始，每 3 行取一次，城市名稱在 i+1 行的第 0 欄
for i in range(8, len(df)-3, 3):
    # print(df.loc[9][0])
    city = str(df.loc[i + 1][0]).replace(" ", "").strip()
    moved_in = df.loc[i][2]
    moved_out = df.loc[i][17]

    if pd.isna(city):
        continue

    total_in[city] = total_in.get(city, 0) + int(moved_in)
    total_out[city] = total_out.get(city, 0) + int(moved_out)

# 建立整理表格
summary = pd.DataFrame({
    '縣市': custom_order,
    '遷入': [total_in.get(city, 0) for city in custom_order],
    '遷出': [total_out.get(city, 0) for city in custom_order]
})
print(summary)
# 輸出 CSV
summary.to_csv('2024縣市人口遷移總人數.csv', index=False, encoding='utf-8')

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 畫直方圖
plt.figure(figsize=(12, 8))
x = range(len(custom_order))
plt.bar(x, summary['遷入'], label='遷入', align='center', color='skyblue')
plt.bar(x, -summary['遷出'], label='遷出', align='center', color='salmon')
plt.xticks(x, custom_order, rotation=45, ha='right')
plt.ylabel('人口數')
plt.title('2024年各縣市遷入遷出人口統計')
plt.legend()
plt.tight_layout()
plt.savefig('遷徙圖表_2024.png')
plt.show()
