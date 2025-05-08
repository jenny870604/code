import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# 讀取資料
file_path='./subject/Age/縣市人口按性別及五齡組(63).xls'

for year in range(102, 114): 
    sheet_name = str(year)
    try:
        df_Age = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    except:
        print(f"無法讀取工作表 {sheet_name}，跳過")
        continue


# 年齡區間對應的欄位位置
# 0歲：欄3
# 1–4歲：欄4
# 接下來每5歲一組：欄9開始
    age_labels = ['0', '1~4']
    male_counts = [df_Age.iloc[5, 3], df_Age.iloc[5, 4]]
    female_counts = [df_Age.iloc[6, 3], df_Age.iloc[6, 4]]

    col = 9
    current_age = 5
    while True:
        try:
            male = df_Age.iloc[5, col]
            female = df_Age.iloc[6, col]
            if pd.isna(male) or pd.isna(female):
                break
            age_labels.append(f'{current_age}~{current_age + 4}')
            male_counts.append(male)
            female_counts.append(female)
            current_age += 5
            col += 1
        except IndexError:
            break

    # 設定中文字型
    fontManager.addfont("ChineseFont.ttf")
    mlp.rc("font", family="ChineseFont")

    # 轉為萬人
    male_counts = [-x / 10000 for x in male_counts]
    female_counts = [x / 10000 for x in female_counts]

    # 繪圖
    plt.figure(figsize=(10, 8))
    y_pos = range(len(age_labels))
    plt.barh(y_pos, male_counts, color='skyblue', label='男性')
    plt.barh(y_pos, female_counts, color='lightpink', label='女性')
    plt.yticks(y_pos, age_labels)
    plt.xlabel('人數（萬人）')
    plt.title(f'{sheet_name} 年人口金字塔')
    plt.legend()
    plt.tight_layout()
    plt.gca().invert_yaxis()

    # 儲存圖檔
    plt.savefig(f'./subject/Age/人口結構_{year}.png')
    plt.close()


