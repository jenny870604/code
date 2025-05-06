import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors

# 讀取檔案
df_actual = pd.read_csv("./subject/population/2013-2024各縣市總人口數.csv")
df_forecast_raw = pd.read_csv("./subject/Predict/2024_人口預測.csv")
# print(df_forecast.iloc[2][0])
# 處理實際人口（最後一欄是2024年人口）
actual_cities = []
actual_pops = []

for i in range(len(df_actual)):
    city = df_actual.iloc[i][0]
    pop = df_actual.iloc[i][-1]
    actual_cities.append(city)
    actual_pops.append(pop)

df_actual_2024 = pd.DataFrame({
    '縣市': actual_cities,
    '實際人口': actual_pops
})

# 處理預測資料
forecast_data = []

# LinearRegression (i=0, i+=2)
for i in range(0, len(df_forecast_raw), 2):
    city = df_forecast_raw.iloc[i][0]
    model = df_forecast_raw.iloc[i][1]
    pred = df_forecast_raw.iloc[i][3]
    forecast_data.append([city, model, pred])

# RandomForest (i=1, i+=2)
for i in range(1, len(df_forecast_raw), 2):
    city = df_forecast_raw.iloc[i][0]
    model = df_forecast_raw.iloc[i][1]
    pred = df_forecast_raw.iloc[i][3]
    forecast_data.append([city, model, pred])

df_forecast = pd.DataFrame(forecast_data, columns=['縣市', '模型', '預測人口'])

# 合併實際與預測
df_merge = df_forecast.merge(df_actual_2024, on='縣市', how='inner')

# 計算誤差指標
df_merge['MAE'] = abs(df_merge['預測人口'] - df_merge['實際人口'])
df_merge['MAPE'] = abs(df_merge['預測人口'] - df_merge['實際人口']) / df_merge['實際人口'] * 100
df_merge['MSE'] = (df_merge['預測人口'] - df_merge['實際人口']) ** 2

# 自訂縣市排序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]
df_merge['縣市'] = pd.Categorical(df_merge['縣市'], categories=custom_order, ordered=True)
df_merge = df_merge.sort_values(['模型', '縣市'])

# 分別輸出模型結果
for model in df_merge['模型'].unique():
    print(f"\n模型: {model}")
    df_model = df_merge[df_merge['模型'] == model]
    print(df_model[['縣市', '預測人口', '實際人口', 'MAE', 'MAPE']])

    mae = df_model['MAE'].mean()
    rmse = np.sqrt(df_model['MSE'].mean())
    mape = df_model['MAPE'].mean()

    print(f"\n→ {model} 整體準確度:")
    print(f"MAE : {mae:,.0f}")
    print(f"RMSE: {rmse:,.0f}")
    print(f"MAPE: {mape:.2f}%")

# 將結果輸出為 CSV
df_merge.to_csv("./subject/Predict/人口預測誤差比較_2024.csv", index=False, encoding='utf-8')

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 準備資料（根據 df_merge）
linear_pred = df_merge[df_merge['模型'] == 'LinearRegression'].sort_values('縣市')
rf_pred = df_merge[df_merge['模型'] == 'RandomForest'].sort_values('縣市')
actual = df_actual_2024.copy()
actual = actual.set_index('縣市').loc[linear_pred['縣市']].reset_index()

labels = linear_pred['縣市'].tolist()
x = np.arange(len(labels))  # x 軸位置
width = 0.25  # 每個長條的寬度

plt.figure(figsize=(18, 8))
plt.plot(x , linear_pred['預測人口']/10000,  label='LinearRegression', marker='o')
plt.plot(x, rf_pred['預測人口']/10000,  label='RandomForest', linestyle='--', marker='x')
plt.plot(x , actual['實際人口']/10000,  label='實際人口', linestyle='--', marker='s')

plt.xlabel('縣市')
plt.ylabel('人口數')
plt.title('各縣市人口預測比較（LinearRegression vs RandomForest vs 實際）')
plt.xticks(x, labels, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# 游標互動標註
cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_add(sel):
    idx = sel.index
    x_label = labels[idx]  # 對應的縣市名稱
    y = sel.artist.get_ydata()[idx]
    sel.annotation.set(text=f"{model}\n縣市:{x_label}\n人口: {int(y):}（萬）")

# 儲存圖片
plt.savefig("./subject/Predict/人口預測比較圖_2024.png", dpi=300)
plt.show()