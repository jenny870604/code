import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# 讀取 Excel 檔案
file_path='./subject/Age/縣市人口按性別及五齡組(63).xls'

# 選擇要處理的工作表，例如 '113'
sheet_name = '113'

# 讀取指定工作表
df_Age = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

# 年齡區間對應的欄位位置
# 0歲：欄3
# 1–4歲：欄4
# 接下來每5歲一組：欄9開始
age_labels = ['0', '1-4']
male_counts = [df_Age.iloc[5, 3], df_Age.iloc[5, 4]]
female_counts = [df_Age.iloc[6, 3], df_Age.iloc[6, 4]]

# 5歲齡區間（從欄9開始）
col = 9
while True:
    try:
        male = df_Age.iloc[5, col]
        female = df_Age.iloc[6, col]
        if pd.isna(male) or pd.isna(female):
            break
        age_range = f'{5*(len(age_labels)-2)}-{5*(len(age_labels)-2)+4}'
        age_labels.append(age_range)
        male_counts.append(male)
        female_counts.append(female)
        col += 1
    except IndexError:
        break

# 將男性人數轉為負數以便畫出對稱金字塔
male_counts = [-x for x in male_counts]
print(male_counts)

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 畫圖
plt.figure(figsize=(10, 8))
y_pos = range(len(age_labels))
plt.barh(y_pos, male_counts, color='skyblue', label='男性')
plt.barh(y_pos, female_counts, color='lightpink', label='女性')
plt.yticks(y_pos, age_labels)
plt.xlabel('人數')
plt.title(f'{sheet_name} 年人口金字塔')
plt.legend()
plt.tight_layout()
plt.gca().invert_yaxis()  # 年齡由小到大從下往上
plt.show()
