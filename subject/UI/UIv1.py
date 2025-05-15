import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# 資料載入
df = pd.read_csv("./subject/population/2013-2024各縣市總人口數.csv")              
pred_df = pd.read_csv("./subject/Predict/2024_人口預測.csv")
# 讀取對應年份的 .xls 檔案
file_age = './subject/Age/縣市人口按性別及五齡組(63).xls'

# 將資料轉
df = df.rename(columns={"Unnamed: 0": "縣市"})
year_columns = [str(y) for y in range(2015, 2025)]
df_long = df.melt(id_vars="縣市", value_vars=year_columns, var_name="年份", value_name="總人口")

# 清洗總人口欄位，移除逗號並轉成整數
df_long["總人口"] = df_long["總人口"].replace(",", "").astype(int)

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 主視窗
root = tk.Tk()
root.title("台灣人口統計分析與預測系統")
root.geometry("1400x800")

frame = tk.LabelFrame(root, text="", padx=10, pady=10)
frame.pack(pady=10)

years = [str(y) for y in range(2015, 2025)]
cities = ['全台'] + [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

def draw_population(fig,year,city):
    # 取得該城市從 2015 ~ 選定年份 的資料
    year_range = [y for y in years if y <= year]
    ax1 = fig.add_subplot(221)

    if city != "全台":
        city_data = df_long[
            (df_long["縣市"] == city) &
            (df_long["年份"].astype(str).isin(year_range))
            ]
        y_values = city_data["總人口"] / 10000
        ax1.plot(city_data["年份"], y_values, marker="o")
    else:
        city_data = df_long[
                df_long["年份"].isin(year_range)
            ]
        # 為每個縣市畫一條線
        for city_name in city_data["縣市"].unique():
            sub_data = city_data[city_data["縣市"] == city_name]
            ax1.plot(sub_data["年份"], sub_data["總人口"] / 10000, marker="o", label=city_name)
            ax1.legend(bbox_to_anchor=(1, 1), loc="upper left", fontsize="small")
            y_values = city_data["總人口"] / 10000
            
    y_min = y_values.min()
    y_max = y_values.max()
    buffer = (y_max - y_min) * 0.05
    y_min -= buffer
    y_max += buffer

    ax1.set_title(f"{city} 歷年總人口變化")
    ax1.set_xlabel("年")
    ax1.set_ylabel("人口數(萬)")
    ax1.set_ylim(y_min, y_max)
    ax1.grid(True)

def draw_Age(fig, df_age, row_idx, title):
    age_labels = ['0', '1~4']
    male_counts = [df_age.iloc[row_idx, 3], df_age.iloc[row_idx, 4]]
    female_counts = [df_age.iloc[row_idx + 1, 3], df_age.iloc[row_idx + 1, 4]]

    col = 9
    current_age = 5
    while True:
        try:
            male = df_age.iloc[row_idx, col]
            female = df_age.iloc[row_idx + 1, col]
            if pd.isna(male) or pd.isna(female):
                break
            age_labels.append(f'{current_age}~{current_age + 4}')
            male_counts.append(male)
            female_counts.append(female)
            current_age += 5
            col += 1
        except IndexError:
            break

    ax = fig.add_subplot(222)
    y = range(len(age_labels))
    ax.barh(y, [-x / 10000 for x in male_counts], color='skyblue', label='男性')
    ax.barh(y, [x / 10000 for x in female_counts], color='lightcoral', label='女性')
    ax.set_yticks(y)
    ax.set_yticklabels(age_labels)
    ax.set_xlabel('人口數(萬)')
    ax.set_title(f'{title} 人口金字塔圖')
    ax.invert_yaxis()
    ax.legend()

#下拉式選單
dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=10)

#讓整體置中
inner_frame = tk.Frame(dropdown_frame)
inner_frame.pack(anchor="center")  

year_var = tk.StringVar()
year_combobox = ttk.Combobox(inner_frame, textvariable=year_var, values=years, state="readonly")
year_combobox.set("年分")
year_combobox.grid(row=0, column=0, padx=10)

city_var = tk.StringVar()
city_combobox = ttk.Combobox(inner_frame, textvariable=city_var, values=cities, state="readonly")
city_combobox.set("縣市")
city_combobox.grid(row=0, column=1, padx=10)

#只用來放圖表，每次查詢會清空重畫
plot_frame = tk.Frame(root)
plot_frame.pack(pady=10)

# 查詢按鈕
def on_submit():
    for widget in plot_frame.winfo_children():
        widget.destroy()
    fig = Figure(figsize=(18, 15), dpi=80)
    fig.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.05)

    year = year_var.get()
    city = city_var.get()
    result_label.config(text=f"查詢：{year} 年 {city}")
    df_age = pd.read_excel(file_age, sheet_name=str(int(year) - 1911), header=None)

    # 建立查詢縣市對應的 row index
    county_index_map = {}
    for i in range(8, len(df_age), 3):
        county_raw = df_age.iloc[i][0]
        if pd.isna(county_raw):
            continue
        county = str(county_raw).replace(" ", "").strip()
        if county in cities:
            county_index_map[county] = i

    if city != "全台":
        # 人口折線圖
        draw_population(fig,year,city)

        i = county_index_map.get(city)
        if i is None:
            return
        
        # 金字塔圖
        draw_Age(fig,df_age,i,city)

        
  
    else:
        # 人口折線圖
        draw_population(fig,year,city)

        # 金字塔圖：全台總和
        # draw_Age(fig, df_age, 5, year)

        # 各縣市總人口長條圖
        pop_yr = df_long[df_long["年份"] == year]
        pop_yr = pop_yr.sort_values("總人口", ascending=False)

        ax2 = fig.add_subplot(222)
        ax2.bar(pop_yr["縣市"], pop_yr["總人口"]/10000)
        ax2.set_title(f"{year} 各縣市人口排行")
        ax2.set_ylabel("人口(萬)")
        ax2.tick_params(axis='x', rotation=45) 
    
    if year=='2024':
        # 處理實際人口（最後一欄是2024年人口）
        actual_cities = []
        actual_pops = []

        for i in range(len(df)):
            city = df.iloc[i][0]
            pop = df.iloc[i][-1]
            actual_cities.append(city)
            actual_pops.append(pop)

        df_actual_2024 = pd.DataFrame({
            '縣市': actual_cities,
            '實際人口': actual_pops
        })

        # 處理預測資料
        forecast_data = []
        # LinearRegression
        for i in range(0, len(pred_df), 2):
            city = pred_df.iloc[i][0]
            model = pred_df.iloc[i][1]
            pred = pred_df.iloc[i][3]
            forecast_data.append([city, model, pred])
        
        # RandomForest
        for i in range(1, len(pred_df), 2):
            city = pred_df.iloc[i][0]
            model = pred_df.iloc[i][1]
            pred = pred_df.iloc[i][3]
            forecast_data.append([city, model, pred])

        df_forecast = pd.DataFrame(forecast_data, columns=['縣市', '模型', '預測人口'])
        df_merge = df_forecast.merge(df_actual_2024, on='縣市', how='inner')

        # 計算誤差指標
        df_merge['MAE'] = abs(df_merge['預測人口'] - df_merge['實際人口'])
        df_merge['MAPE'] = abs(df_merge['預測人口'] - df_merge['實際人口']) / df_merge['實際人口'] * 100
        df_merge['MSE'] = (df_merge['預測人口'] - df_merge['實際人口']) ** 2

        df_merge['縣市'] = pd.Categorical(df_merge['縣市'], categories=cities[1:], ordered=True)
        df_merge = df_merge.sort_values(['模型', '縣市'])

        linear_pred = df_merge[df_merge['模型'] == 'LinearRegression'].sort_values('縣市')
        rf_pred = df_merge[df_merge['模型'] == 'RandomForest'].sort_values('縣市')
        actual = df_actual_2024.copy()
        actual = actual.set_index('縣市').loc[linear_pred['縣市']].reset_index()

        labels = linear_pred['縣市'].tolist()
        x = np.arange(len(labels))
        width = 0.25

        # fig, ax = plt.subplots(figsize=(18, 8))
        ax3 = fig.add_subplot(223)
        ax3.plot(x , linear_pred['預測人口']/10000,  label='LinearRegression', marker='o')
        ax3.plot(x, rf_pred['預測人口']/10000,  label='RandomForest', linestyle='--', marker='x')
        ax3.plot(x , actual['實際人口']/10000,  label='實際人口', linestyle='--', marker='s')

        ax3.set_xlabel('縣市')
        ax3.set_ylabel('人口數 (萬)')
        ax3.set_title('各縣市人口預測比較（LinearRegression vs RandomForest vs 實際）')
        ax3.set_xticks(x)
        ax3.set_xticklabels(labels, rotation=45, ha='right')
        ax3.legend()
        fig.tight_layout()
               
    # 顯示圖表在 Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

submit_button = tk.Button(inner_frame, text="查詢", command=on_submit)
submit_button.grid(row=0, column=2, padx=10)

result_label = tk.Label(inner_frame, text="", font=("Arial", 12))
result_label.grid(row=0, column=3, padx=10)

root.mainloop()