import pandas as pd

# 讀取資料
df_population = pd.read_csv('./subject/population/2013-2024各縣市總人口數.csv')
df_birth = pd.read_csv('./subject/Born/2015-2024出生人數.csv')
df_death = pd.read_csv('./subject/Death/死亡人數2015-2024.csv')
df_move_in = pd.read_csv('./subject/Move/2015-2024縣市人口遷入統計.csv')
df_move_out = pd.read_csv('./subject/Move/2015-2024縣市人口遷出統計.csv')

# 改名統一
df_population.rename(columns={'Unnamed: 0': '縣市'}, inplace=True)
df_birth.rename(columns={'Unnamed: 0': '縣市'}, inplace=True)
df_death.rename(columns={'Unnamed: 0': '縣市'}, inplace=True)
df_move_in.rename(columns={'Unnamed: 0': '縣市'}, inplace=True)
df_move_out.rename(columns={'Unnamed: 0': '縣市'}, inplace=True)
# print(df_move_out)
# 準備年份
years = [str(y) for y in range(2015, 2025)]

# 建立新 DataFrame
rows = []
for year in years:
    for index, row in df_population.iterrows():
        county = row['縣市']
        total_pop = row[year]
        birth = df_birth.loc[df_birth['縣市'] == county, year].values[0]
        death = df_death.loc[df_death['縣市'] == county, year].values[0]
        move_in = df_move_in.loc[df_move_in['縣市'] == county, year].values[0]
        move_out = df_move_out.loc[df_move_out['縣市'] == county, year].values[0]
        print(birth)

        net_migration = move_in - move_out #淨遷徙人數
        natural_increase = birth - death #自然增加人數

        prev_year = str(int(year) - 1)
        if prev_year in df_population.columns:
            prev_pop = df_population.loc[df_population['縣市'] == county, prev_year].values[0]
            pop_change = total_pop - prev_pop
            try:
                growth_rate = round((pop_change / prev_pop) * 100, 2)
            except ZeroDivisionError:
                growth_rate = 0
        else:
            pop_change = None
            growth_rate = None

        rows.append({
            '年份': int(year),
            '縣市': county,
            '總人口': f"{int(total_pop):,}",
            '出生人數': f"{int(birth):,}",
            '死亡人數': f"{int(death):,}",
            '遷入人數': f"{int(move_in):,}",
            '遷出人數': f"{int(move_out):,}",
            '淨遷徙人數': f"{net_migration:+,}",
            '自然增加人數': f"{natural_increase:+,}",
            '年人口變動': f"{pop_change:+,}" if pop_change is not None else '',
            '年增率（%）': f"{growth_rate:+.2f}" if growth_rate is not None else ''
        })


# 建立輸出 DataFrame
result_df = pd.DataFrame(rows)

# 儲存 CSV
result_df.to_csv('./subject/Predict/整合人口統計.csv', index=False, encoding='utf-8-sig')
