import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

files = {
    2015: "./subject/Move/縣市遷入及遷出(按登記)-104年.xls",
    2016: "./subject/Move/縣市遷入及遷出(按登記)-105年.xls",
    2017: "./subject/Move/縣市遷入及遷出(按登記)-106年.xls",
    2018: "./subject/Move/縣市遷入及遷出(按登記)-107年.xls",
    2019: "./subject/Move/縣市遷入及遷出(按登記)-108年.xls",
    2020: "./subject/Move/縣市遷入及遷出(按登記)-109年.xls",
    2021: "./subject/Move/縣市遷入及遷出(按登記)-110年.xls",
    2022: "./subject/Move/縣市遷入及遷出(按登記)-111年.xls",
    2023: "./subject/Move/縣市遷入及遷出(按登記)-112年.xls",
    2024: "./subject/Move/縣市遷入及遷出(按登記)-113年.xls",
}

# 儲存結果
def extract_migration_data(file_path, year):
    sheet_name = '01-12月合計' if year == 2015 else '01-12累計'
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    records = []
    for i in range(8, len(df) - 3, 3):
        city = str(df.loc[i+1][0]).replace(" ", "").strip()
        inm = pd.to_numeric(df.loc[i][2], errors='coerce')
        outm = pd.to_numeric(df.loc[i][17], errors='coerce')
        records.append({'年度': year, 
                        '縣市': city, 
                        '遷入': inm, 
                        '遷出': outm})
    return records

data = []
for year, path in files.items():
    data.extend(extract_migration_data(path, year))

# 將之前取得的資料轉成 DataFrame
df_result = pd.DataFrame(data)

# 遷入與遷出資料分別建立寬格式表格
in_df = df_result.pivot(index='縣市', columns='年度', values='遷入')
out_df = df_result.pivot(index='縣市', columns='年度', values='遷出')

# 建立 MultiIndex 欄位（上層為 遷入/遷出，下層為 年份）
in_df.columns = pd.MultiIndex.from_product([['遷入'], in_df.columns])
out_df.columns = pd.MultiIndex.from_product([['遷出'], out_df.columns])

# 將 MultiIndex 欄位轉成單層欄位，只保留年份
in_df.columns = in_df.columns.get_level_values(1)
out_df.columns = out_df.columns.get_level_values(1)

# 按照自訂縣市排序
in_df = in_df.loc[custom_order]
out_df = out_df.loc[custom_order]

# 移除 index 名稱（讓 CSV 不會出現「縣市」字樣）
in_df.index.name = None
out_df.index.name = None
# print(in_df)
# 輸出為 CSV
in_df.to_csv('2015-2024縣市人口遷入統計.csv')
out_df.to_csv('2015-2024縣市人口遷出統計.csv')

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 繪製每一年的遷徙圖表
for year in range(2015, 2025):
    df_year = df_result[df_result['年度'] == year]
    
    # 若該年資料不完整則略過
    if df_year.empty:
        continue

    # 確保按照自訂順序排序
    df_year = df_year.set_index('縣市').loc[custom_order].reset_index()

    plt.figure(figsize=(12, 7))
    x = df_year['縣市']
    plt.bar(x, df_year['遷入'], label='遷入', color='skyblue')
    plt.bar(x, -df_year['遷出'], label='遷出', color='salmon')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('人數')
    plt.title(f'{year}年各縣市遷入與遷出人數')
    plt.legend()
    plt.tight_layout()
    
    output_png = f'遷徙圖表_{year}.png'
    plt.savefig(output_png, dpi=300)
    plt.close()
