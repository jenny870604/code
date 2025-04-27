import requests
import pandas as pd

url = "https://od.moi.gov.tw/api/v1/rest/datastore/301000000A-000605-079"
response = requests.get(url)
data = response.json()
records = data['result']['records']
df = pd.DataFrame(records)

# 只留下有「市」或「縣」的區域資料
df = df[df['site_id'].str.contains('市|縣') & (df['site_id'].str.len() <= 8)]

def extract_city(site_id):
    if '縣' in site_id:
        return site_id.split('縣')[0] + '縣'
    elif '市' in site_id:
        return site_id.split('市')[0] + '市' 
    else:
        return site_id

df['city'] = df['site_id'].apply(extract_city)
df['people_total'] = pd.to_numeric(df['people_total'], errors='coerce')

city_population = df.groupby('city')['people_total'].sum().reset_index()
# city_population=city_population.sort_values(by='people_total', ascending=False)
# 排序
custom_order = [
    '基隆市', '新北市', '臺北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '臺中市', '南投縣', 
    '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

# 把 city 欄位轉成 Categorical，指定順序
city_population['city'] = pd.Categorical(city_population['city'], categories=custom_order, ordered=True)

# 根據這個順序排序
city_population = city_population.sort_values('city').reset_index(drop=True)

print(city_population)
