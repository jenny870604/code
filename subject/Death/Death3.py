import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

# 自訂順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

### 讀取2015-2023年資料 ###
xls = pd.ExcelFile("./subject/Death/縣市死亡人口按五齡組(按發生)(96).xls")
all_data = pd.DataFrame()

for year in range(2015, 2024):  # 104~112
    sheet_name = str(year-1911)
    df = xls.parse(sheet_name)
    data = []
    for i in range(8, len(df), 3):
        city = str(df.iloc[i, 0]).replace(" ", "").strip()
        death = df.iloc[i - 1, 2]
        data.append({"縣市": city, str(year): death})
    year_df = pd.DataFrame(data)
    if all_data.empty:
        all_data = year_df
    else:
        all_data = pd.merge(all_data, year_df, on="縣市", how="outer")

### 讀取2024年資料 ###
xls_path = './subject/Death/縣市出生死亡結婚離婚(按登記)-113年.xls'
df_2024 = pd.read_excel(xls_path, sheet_name='縣市全年出生率、結婚率等')
death_data_2024 = df_2024.loc[3:, [df_2024.columns[0], df_2024.columns[3]]]
death_data_2024.columns = ['縣市', '2024']
death_data_2024['縣市'] = death_data_2024['縣市'].astype(str).str.replace(r'\s+', '', regex=True)
death_data_2024 = death_data_2024[
    death_data_2024['縣市'].isin(custom_order) & 
    (death_data_2024['縣市'].str.len() < 8)
]

### 合併2024年資料 ###
all_data["sort_key"] = all_data["縣市"].apply(lambda x: custom_order.index(x) if x in custom_order else -1)
all_data = all_data[all_data["sort_key"] >= 0].sort_values("sort_key").drop("sort_key", axis=1)
death_data_2024 = death_data_2024[["縣市", "2024"]]
combined_data = pd.merge(all_data, death_data_2024, on="縣市", how="left")

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

### 畫圖 ###
combined_data_sorted = combined_data.copy()
combined_data_sorted["排序"] = combined_data_sorted["縣市"].apply(lambda x: custom_order.index(x))
combined_data_sorted = combined_data_sorted.sort_values("排序").drop(columns=["排序"])

combined_data_sorted.set_index("縣市").T.plot(figsize=(12, 8), marker='o')
plt.title("2015~2024年各縣市死亡人數")
plt.xlabel("年份")
plt.ylabel("死亡人數")
plt.grid(True)
plt.legend(title="縣市", bbox_to_anchor=(1.05, 1), loc='upper left')

# 游標互動標註
cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_add(sel):
    line = sel.artist
    x, y = sel.target
    city = line.get_label()
    sel.annotation.set_text(f"{city}\n死亡人數: {int(y)}")

plt.tight_layout()
plt.savefig("死亡人數2015-2024.png")
plt.show()

### 輸出 CSV ###
combined_data_sorted.to_csv("死亡人數2015-2024.csv", index=False, encoding="utf-8")
