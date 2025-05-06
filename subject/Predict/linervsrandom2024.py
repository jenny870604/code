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
error_metrics = []

models = {
    'LinearRegression': LinearRegression(),
    'RandomForest': RandomForestRegressor(random_state=1)
}

for city, group in df_selected.groupby('縣市'):
    X = group[features]
    y = group[target]
    years = group['年份'].values

    for model_name, model in models.items():
        model.fit(X, y)
        y_pred = model.predict(X)

        # 儲存每年預測結果
        for i in range(len(years)):
            all_predictions.append({
                '縣市': city,
                '模型': model_name,
                '年份': years[i],
                '實際人口': int(round(y.iloc[i])),
                '預測人口': int(round(y_pred[i]))
            })

        # 計算誤差指標
        mae = mean_absolute_error(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        mape = (abs((y - y_pred) / y) * 100).mean()

        error_metrics.append({
            '縣市': city,
            '模型': model_name,
            'MAE': mae,
            'MSE': mse,
            'MAPE': mape
        })

# 轉為 DataFrame
pred_df = pd.DataFrame(all_predictions)

# 整理為 DataFrame 並依自定義順序排序
results_df = pd.DataFrame(all_predictions)
results_df['排序'] = results_df['縣市'].apply(lambda x: custom_order.index(x))
results_df = results_df.sort_values(['排序']).drop(columns='排序')
# print(results_df.head())
error_df = pd.DataFrame(error_metrics)
error_df = error_df.sort_values(by='縣市', key=lambda x: x.map(lambda city: custom_order.index(city)))
error_df.to_csv('./subject/Predict/人口預測誤差指標.csv', index=False, encoding='utf-8')