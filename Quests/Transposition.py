import pandas as pd
import calendar
from datetime import datetime
import random

# Lista firm
companies = ["FirmaA", "FirmaB", "FirmaC"]

# Zakres lat i miesięcy
start_year = 2023
end_year = 2024

# Generowanie nazw kolumn: YYYY-MM-last_day
columns = []
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]
        col_name = f"{year}-{month:02d}-{last_day:02d}"
        columns.append(col_name)

# Budowanie danych
data = []
for company in companies:
    revenues = [random.randint(10000, 200000) for _ in columns]
    row = [company] + revenues
    data.append(row)

# Tworzenie DataFrame


df = pd.DataFrame(data, columns=["firma"] + columns)



df_t = df.T
df_t.columns = df_t.iloc[0]   # pierwszy wiersz → nazwy kolumn
df_t = df_t.iloc[1:]          # usuń pierwszy wiersz

print(df_t.head())

