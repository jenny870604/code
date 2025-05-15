import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp


# 讀取 Excel 檔案與指定工作表
file_path = './subject/Age/縣市人口按性別及五齡組(63).xls'
sheet_name = '113'
df_Age = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

# 自訂縣市排序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 繪製每個縣市的人口金字塔圖
for i in range(8, len(df_Age), 3):  # 每3列是一組男、女、總計
    county_raw = df_Age.iloc[i][0]
    if pd.isna(county_raw):
        continue
    county = str(county_raw).replace(" ", "").strip() # 去除空白格
    print(county)

    if county not in custom_order:
        continue

    # 解析年齡區間與男女人口
    age_labels = ['0', '1-4']
    male_counts = [df_Age.iloc[i, 3], df_Age.iloc[i, 4]]
    female_counts = [df_Age.iloc[i+1, 3], df_Age.iloc[i+1, 4]]

    col = 9
    while True:
        try:
            male = df_Age.iloc[i, col]
            female = df_Age.iloc[i+1, col]
            if pd.isna(male) or pd.isna(female):
                break
            age_range = f'{5*(len(age_labels)-2)}-{5*(len(age_labels)-2)+4}'
            age_labels.append(age_range)
            male_counts.append(male)
            female_counts.append(female)
            col += 1
        except IndexError:
            break

    # 設定中文字型
    fontManager.addfont("ChineseFont.ttf")
    mlp.rc("font", family="ChineseFont")

    # 建立金字塔圖
    plt.figure(figsize=(10, 6))
    y = range(len(age_labels))
    plt.barh(y, [-x for x in male_counts], color='skyblue', label='男性')
    plt.barh(y, female_counts, color='lightcoral', label='女性')
    plt.yticks(y, age_labels)
    plt.xlabel('人口數')
    plt.title(f'{county} 人口金字塔圖')
    plt.legend()
    plt.tight_layout()
    plt.show()
