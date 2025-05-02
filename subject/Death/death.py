import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# 讀取 xls 檔案中所有的工作表名稱
xls_path = './subject/Death/縣市出生死亡結婚離婚(按登記)-113年.xls'
df = pd.read_excel(xls_path, sheet_name='縣市全年出生率、結婚率等')  # 工作表名稱是 '縣市全年出生率、結婚率等'

# 自定義順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# row_2 = df.iloc[1]  # 讀取第2列
# print(row_2)
# print(df.loc[4][3])

# 假設第0欄是縣市名稱，第3欄是死亡人數
# 擷取需要的資料（從第3列開始）
death_data = df.loc[3:, [df.columns[0], df.columns[3]]]
death_data.columns = ['縣市', '死亡人數']

# 移除空白與轉為文字格式方便比對
death_data['縣市'] = death_data['縣市'].astype(str).str.replace(r'\s+', '', regex=True)

#過濾符合 custom_order 且字串長度 < 8
death_data = death_data[
    death_data['縣市'].isin(custom_order) & 
    (death_data['縣市'].str.len() < 8)
]
print(death_data)

# print(death_data)
# 依照 custom_order 排序
death_data['排序'] = death_data['縣市'].apply(lambda x: custom_order.index(x))
death_data = death_data.sort_values('排序')

# 儲存成 CSV
death_data_to_csv = death_data[['縣市', '死亡人數']].copy()
death_data_to_csv.columns = ['', '2024']
death_data_to_csv.to_csv("死亡人數2024.csv", index=False, encoding='utf-8')

# 設定中文字體
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 畫圖並儲存成 PNG
plt.figure(figsize=(12, 6))
plt.bar(death_data['縣市'], death_data['死亡人數'].astype(int), color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('縣市')
plt.ylabel('死亡人數')
plt.title('各縣市死亡人數')
plt.tight_layout()
plt.savefig("死亡人數2024.png")
plt.show()