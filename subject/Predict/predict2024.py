import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import matplotlib as mlp
import mplcursors


# 讀取資料
df = pd.read_csv("./subject/Predict/整合人口統計.csv")

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

# 自定義縣市順序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣',
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 模型訓練與預測
results = []

for city, group in df_clean.groupby('縣市'):
    X = group[features]
    y = group[target]

    X_train, y_train = X.iloc[:-1], y.iloc[:-1]
    X_test = X.iloc[-1:]
    year = group.iloc[-1]['年份'] + 1

    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(random_state=1)
    }

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)[0]
        results.append({
            '縣市': city,
            '模型': model_name,
            '預測年份': year,
            '預測人口': int(round(y_pred))
        })

# 整理為 DataFrame 並依自定義順序排序
results_df = pd.DataFrame(results)
results_df['排序'] = results_df['縣市'].apply(lambda x: custom_order.index(x))
results_df = results_df.sort_values(['排序', '模型']).drop(columns='排序')

# 顯示預測結果
print(results_df)

# 儲存為 CSV
csv_output_path = "./subject/Predict/2024_人口預測.csv"
results_df.to_csv(csv_output_path, index=False)

# 設定中文字型
fontManager.addfont("ChineseFont.ttf")
mlp.rc("font", family="ChineseFont")

# 繪圖
fig, ax = plt.subplots(figsize=(14, 8))
for model in results_df['模型'].unique():
    subset = results_df[results_df['模型'] == model]
    ax.plot(subset['縣市'], subset['預測人口']/10000, marker='o', label=model)

plt.xticks(rotation=45, ha='right')
plt.ylabel('預測人口數')
plt.title('2024 年各縣市人口預測')
plt.legend()
plt.tight_layout()

# 游標互動標註
cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_add(sel):
    model = sel.artist.get_label()
    x, y = sel.target
    sel.annotation.set(text=f"{model}\n人口: {int(y):}（萬）")


# 儲存圖片
image_output_path = "./subject/Predict/2024_人口預測圖.png"
plt.savefig(image_output_path)
plt.show()
