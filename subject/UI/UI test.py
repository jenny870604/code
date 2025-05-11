import tkinter as tk
from tkinter import ttk

# 建立主視窗
root = tk.Tk()
root.title("台灣人口統計分析與預測系統")
root.geometry("600x200")

# 標題框
frame = tk.LabelFrame(root, text="", padx=10, pady=10)
frame.pack(pady=10)
# title_label = tk.Label(frame, text="台灣人口統計分析與預測系統", font=("Arial", 16))
# title_label.pack()

# 下拉選單資料
years = [str(y) for y in range(2015, 2025)]
cities = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 下拉選單容器
dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=10)

# 年分選單
year_var = tk.StringVar()
year_combobox = ttk.Combobox(dropdown_frame, textvariable=year_var, values=years, state="readonly")
year_combobox.set("年分")
year_combobox.grid(row=0, column=0, padx=10)

# 縣市選單
city_var = tk.StringVar()
city_combobox = ttk.Combobox(dropdown_frame, textvariable=city_var, values=cities, state="readonly")
city_combobox.set("縣市")
city_combobox.grid(row=0, column=1, padx=10)

# 查詢按鈕
def on_submit():
    year = year_var.get()
    city = city_var.get()
    result = f"你查詢的是：{year} 年 {city}"
    result_label.config(text=result)

submit_button = tk.Button(dropdown_frame, text="查詢", command=on_submit)
submit_button.grid(row=0, column=2, padx=10)

# 結果顯示
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()