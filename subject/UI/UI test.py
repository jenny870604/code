import tkinter as tk

def on_select_year(value):
    label_year.config(text=f"你選擇的年分：{value}")

def on_select_city(value):
    label_city.config(text=f"你選擇的縣市：{value}")

root = tk.Tk()
root.title("年分與縣市選單")
root.geometry("400x200")

# 年分選項
years = [str(y) for y in range(2015, 2025)]
selected_year = tk.StringVar()
selected_year.set(years[0])
dropdown_year = tk.OptionMenu(root, selected_year, *years, command=on_select_year)
dropdown_year.pack(pady=10)

label_year = tk.Label(root, text="請選擇年分")
label_year.pack()

# 縣市選項
cities = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]
selected_city = tk.StringVar()
selected_city.set(cities[0])
dropdown_city = tk.OptionMenu(root, selected_city, *cities, command=on_select_city)
dropdown_city.pack(pady=10)

label_city = tk.Label(root, text="請選擇縣市")
label_city.pack()

root.mainloop()
