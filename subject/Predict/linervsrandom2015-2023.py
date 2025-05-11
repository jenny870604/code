import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors
from sklearn.metrics import mean_absolute_error, mean_squared_error


# 讀取資料
df = pd.read_csv("./subject/Predict/整合人口統計.csv")

# 自定義縣市順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]


# 數值清理函數
def clean_number(x):
    if isinstance(x, str):
        x = x.replace(',', '').replace('+', '').replace('−', '-').strip()
    try:
        return int(x)
    except:
        try:
            return float(x)
        except:
            return None

# 欄位清理
cols_to_clean = ['總人口', '出生人數', '死亡人數', '淨遷徙人數', '自然增加人數', '年增率（%）']
for col in cols_to_clean:
    df[col] = df[col].apply(clean_number)

# 建立前一年欄位
df = df.sort_values(['縣市', '年份'])
df['前一年總人口'] = df.groupby('縣市')['總人口'].shift(1)
df['前一年自然增加人數'] = df.groupby('縣市')['自然增加人數'].shift(1)
df['前一年年增率'] = df.groupby('縣市')['年增率（%）'].shift(1)

# 移除缺漏值
df_clean = df.dropna(subset=[
    '出生人數', '死亡人數', '淨遷徙人數',
    '前一年總人口', '前一年自然增加人數', '前一年年增率', '總人口'
])

# 特徵與目標
features = ['出生人數', '死亡人數', '淨遷徙人數', '前一年總人口', '前一年自然增加人數', '前一年年增率']
target = '總人口'

df_selected = df_clean[df_clean['縣市'].isin(custom_order)]

# 儲存預測與實際值以作圖
all_predictions = []

for city, group in df_selected.groupby('縣市'):
    X = group[features]
    y = group[target]
    years = group['年份'].values

    # 訓練用資料
    X_train = X
    y_train = y

    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_train)

    # Random Forest
    rf_model = RandomForestRegressor(random_state=1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_train)

    # 儲存結果
    for i in range(len(years)):
        all_predictions.append({
            '縣市': city,
            '年份': years[i],
            '實際人口': y.iloc[i],
            'LinearRegression': y_pred_lr[i],
            'RandomForest': y_pred_rf[i]
        })

# 轉為 DataFrame
pred_df = pd.DataFrame(all_predictions)

# 整理為 DataFrame 並依自定義順序排序
results_df = pd.DataFrame(all_predictions)
results_df['排序'] = results_df['縣市'].apply(lambda x: custom_order.index(x))
results_df = results_df.sort_values(['排序']).drop(columns='排序')
# print(results_df.head())


# 將結果輸出為 CSV
results_df.to_csv("./subject/Predict/人口預測誤差比較_2016-2023.csv", index=False, encoding='utf-8')

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")


# 繪圖
fig, axes = plt.subplots(len(custom_order), 1, figsize=(10, 6 * len(custom_order)), sharex=True)

if len(custom_order) == 1:
    axes = [axes]

for city in custom_order:
    data = pred_df[pred_df['縣市'] == city]

    if data.empty:
        print(f"⚠️ 跳過 {city}，因為沒有可用的預測資料。")
        continue

    plt.figure(figsize=(10, 6))
    plt.plot(data['年份'], data['實際人口']/100000, label='實際人口', marker='o')
    plt.plot(data['年份'], data['LinearRegression']/100000, label='線性回歸預測', linestyle='--', marker='x')
    plt.plot(data['年份'], data['RandomForest']/100000, label='隨機森林預測', linestyle='--', marker='s')
    plt.title(f'{city} 人口預測比較')
    plt.xlabel('年份')
    plt.ylabel('人口數')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f'人口預測_{city}.png')
    plt.close()