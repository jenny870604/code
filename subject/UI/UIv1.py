import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 資料載入
df = pd.read_csv("./subject/population/2013-2024各縣市總人口數.csv")              
pred_df = pd.read_csv("./subject/Predict/2024_人口預測.csv")

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
root.geometry("1200x700")

frame = tk.LabelFrame(root, text="", padx=10, pady=10)
frame.pack(pady=10)

years = [str(y) for y in range(2015, 2025)]
cities = ['全台'] + [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

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
    year = year_var.get()
    city = city_var.get()
    result_label.config(text=f"查詢：{year} 年 {city}")
    
     # 清空原本的圖表 Frame 內容（避免重疊）
    for widget in plot_frame.winfo_children():
        widget.destroy()

    if city != "全台":
        # 取得該城市從 2015 ~ 選定年份 的資料
        year_range = [y for y in years if y <= year]
        city_data = df_long[
            (df_long["縣市"] == city) &
            (df_long["年份"].astype(str).isin(year_range))
            ]
        
        y_values = city_data["總人口"] / 10000
        y_min = y_values.min()
        y_max = y_values.max()
        buffer = (y_max - y_min) * 0.05
        y_min -= buffer
        y_max += buffer

        fig = Figure(figsize=(12, 5), dpi=100)
        ax1 = fig.add_subplot(121)  # 左邊子圖：折線圖
        ax1.plot(city_data["年份"], y_values, marker="o")
        ax1.set_title(f"{city} 歷年總人口變化")
        ax1.set_xlabel("年")
        ax1.set_ylabel("人口數(萬)")
        ax1.set_ylim(y_min, y_max)
        ax1.grid(True)
  
    else:
            # 各縣市總人口長條圖
            pop_yr = df_long[df_long["年份"] == year]
            pop_yr = pop_yr.sort_values("總人口", ascending=False)

            # 建立 Figure 並畫圖
            fig = Figure(figsize=(13, 7), dpi=100)
            ax1 = fig.add_subplot(121)
            ax1.bar(pop_yr["縣市"], pop_yr["總人口"]/10000)
            ax1.set_title(f"{year} 各縣市人口排行")
            ax1.set_ylabel("人口(萬)")
            ax1.tick_params(axis='x', rotation=45)    

             # 金字塔圖：全台總和
            # 讀取對應年份的 .xls 檔案
            xls_path = './subject/Age/縣市人口按性別及五齡組(63).xls'
            try:
                df_age = pd.read_excel(xls_path, sheet_name=str(int(year) - 1911), header=None)
            except:
                df_age = None

            if df_age is not None:
                # 假設全台加總在 row 5（男）與 row 6（女）
                age_labels = ['0', '1~4']
                male_counts = [df_age.iloc[5, 3], df_age.iloc[5, 4]]
                female_counts = [df_age.iloc[6, 3], df_age.iloc[6, 4]]

                col = 9
                current_age = 5
                while True:
                    try:
                        m = df_age.iloc[5, col]
                        f = df_age.iloc[6, col]
                        if pd.isna(m) or pd.isna(f):
                            break
                        age_labels.append(f'{current_age}~{current_age+4}')
                        male_counts.append(m)  # 男性為負
                        female_counts.append(f)
                        current_age += 5
                        col += 1
                    except IndexError:
                        break

                # 轉為萬人
                male_counts = [-x / 10000 for x in male_counts]
                female_counts = [x / 10000 for x in female_counts]

                # 畫金字塔圖
                ax2 = fig.add_subplot(122)
                y_pos = range(len(age_labels))
                ax2.barh(y_pos, male_counts, color='skyblue', label='男性')
                ax2.barh(y_pos, female_counts, color='lightpink', label='女性')
                ax2.set_yticks(y_pos)
                ax2.set_yticklabels(age_labels)
                ax2.set_xlabel('人數（萬人）')
                ax2.set_title(f"{year} 全台人口金字塔")
                ax2.legend()
                ax2.invert_yaxis()        
    # 顯示圖表在 Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

submit_button = tk.Button(inner_frame, text="查詢", command=on_submit)
submit_button.grid(row=0, column=2, padx=10)

result_label = tk.Label(inner_frame, text="", font=("Arial", 12))
result_label.grid(row=0, column=3, padx=10)

root.mainloop()