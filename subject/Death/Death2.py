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

# 讀取 xls 檔案
xls = pd.ExcelFile("./subject/Death/縣市死亡人口按五齡組(按發生)(96).xls")

# 初始化總表
all_data = pd.DataFrame()

# 依序讀取工作表
for year in range(112, 103, -1):  # 112到104
    sheet_name = f"{year}"
    df = xls.parse(sheet_name)

    data = []
    for i in range(8, len(df), 3):
        city = str(df.iloc[i, 0]).replace(" ", "").strip()  # 移除空格與前後空白
        death = df.iloc[i-1, 2]
        data.append({"縣市": city, f"{year+1911}": death})

    year_df = pd.DataFrame(data)
    if all_data.empty:
        all_data = year_df
    else:
        all_data = pd.merge(all_data, year_df, on="縣市", how="outer")

# 將縣市依照 custom_order 排序
all_data["sort_key"] = all_data["縣市"].apply(lambda x: custom_order.index(x) if x in custom_order else -1)
all_data = all_data[all_data["sort_key"] >= 0].sort_values("sort_key").drop("sort_key", axis=1)

# 設定中文字型（避免中文亂碼）
fontManager.addfont("ChineseFont.ttf") #加入字體
mlp.rc("font",family="ChineseFont") #設定使用這個字體

# 畫圖
all_data.set_index("縣市").T.plot(figsize=(12, 8), marker='o')
plt.title("104~112年各縣市死亡人數")
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
plt.savefig("死亡人數2015-2023.png")
plt.show()

all_data_renamed = all_data.copy()
all_data_renamed.columns = [col for col in all_data.columns]
all_data_renamed.to_csv("死亡人數2015-2023.csv", index=False, encoding="utf-8-sig")
