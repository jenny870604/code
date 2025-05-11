import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp

# 資料載入
df = pd.read_csv("./subject/Predict/整合人口統計.csv")
pred_df = pd.read_csv("./subject/Predict/2024_人口預測.csv")

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 主視窗
root = tk.Tk()
root.title("台灣人口統計分析與預測系統")
root.geometry("600x200")

frame = tk.LabelFrame(root, text="", padx=10, pady=10)
frame.pack(pady=10)

years = [str(y) for y in range(2015, 2025)]
cities = ['全台'] + [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=10)

year_var = tk.StringVar()
year_combobox = ttk.Combobox(dropdown_frame, textvariable=year_var, values=years, state="readonly")
year_combobox.set("年分")
year_combobox.grid(row=0, column=0, padx=10)

city_var = tk.StringVar()
city_combobox = ttk.Combobox(dropdown_frame, textvariable=city_var, values=cities, state="readonly")
city_combobox.set("縣市")
city_combobox.grid(row=0, column=1, padx=10)

# 查詢功能邏輯主體
def on_submit():
    year = int(year_var.get())
    city = city_var.get()
    
    result_label.config(text=f"查詢：{year} 年 {city}")
    df["總人口"] = df["總人口"].str.replace(",", "").astype(int)
    if city != "全台":
        city_data = df[df["縣市"] == city]

        y_min = df["總人口"].min()
        y_max = df["總人口"].max()
        buffer = (y_max - y_min) * 0.05
        y_min -= buffer
        y_max += buffer

        # 折線圖（歷年人口）
        plt.figure(figsize=(8,4))
        plt.plot(city_data["年份"], city_data["總人口"], marker="o")
        plt.title(f"{city} 歷年總人口變化")
        plt.xlabel("年")
        plt.ylabel("人口數")
        plt.ylim(y_min, y_max) 
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 金字塔圖（若是單一年份）
        if "年齡層" in df.columns and "性別" in df.columns:
            age_data = city_data[city_data["年份"] == year]
            if not age_data.empty:
                plot_pyramid(age_data)

        # 預測圖（如果是 2024）
        if year == 2024:
            actual = city_data[city_data["年份"] == 2024]["總人口"].values[0]
            pred = pred_df[pred_df["縣市"] == city]["預測人口"].values[0]
            plt.figure()
            plt.bar(["實際", "預測"], [actual, pred], color=["blue", "orange"])
            plt.title(f"{city} 2024 年人口預測 vs 實際")
            plt.ylabel("人口")
            plt.tight_layout()
            plt.show()

    else:
        # 全台資料視覺化
        if year == 2024:
            merged = df[df["年份"] == 2024][["縣市", "總人口"]].merge(
                pred_df, on="縣市", how="left"
            )
            merged = merged.set_index("縣市")[["總人口", "預測人口"]]
            merged.plot(kind="bar", figsize=(10,5), title="2024 各縣市 實際 vs 預測人口")
            plt.ylabel("人口")
            plt.tight_layout()
            plt.show()
        else:
            # 各縣市總人口長條圖
            pop_yr = df[df["年份"] == year]
            pop_yr = pop_yr.sort_values("總人口", ascending=False)
            plt.figure(figsize=(10,5))
            plt.bar(pop_yr["縣市"], pop_yr["總人口"])
            plt.title(f"{year} 各縣市人口排行")
            plt.xticks(rotation=45)
            plt.ylabel("人口")
            plt.tight_layout()
            plt.show()

# 製作金字塔圖的函式（需有年齡層與性別資料）
def plot_pyramid(df_age):
    male = df_age[df_age["性別"] == "男"]
    female = df_age[df_age["性別"] == "女"]
    age_groups = male["年齡層"].tolist()
    male_counts = -male["人口數"].tolist()  # 左側為負數
    female_counts = female["人口數"].tolist()

    plt.figure(figsize=(6,5))
    plt.barh(age_groups, male_counts, color='blue', label='男')
    plt.barh(age_groups, female_counts, color='orange', label='女')
    plt.title("年齡金字塔圖")
    plt.xlabel("人口數")
    plt.legend()
    plt.tight_layout()
    plt.show()

submit_button = tk.Button(dropdown_frame, text="查詢", command=on_submit)
submit_button.grid(row=0, column=2, padx=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
