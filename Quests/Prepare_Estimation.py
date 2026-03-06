from My_Tools.Add_next_date import add_next_date
from My_Tools.Estimate import Wykonaj_Prognozę
from My_Tools.Best_Estimation import najlepsza_prognoza
from statsmodels.tsa.arima.model import ARIMA


dates = [
    "2024-01-01","2024-01-02","2024-01-03",
    "2024-01-04","2024-01-05","2024-01-06",
    "2024-01-07","2024-01-08","2024-01-09"
]

values = [10,12,13,15,18,41,40,43,45]

prognoza = najlepsza_prognoza(dates, values)
prognoza_liczba=Wykonaj_Prognozę(prognoza,dates,values)

values.append(prognoza_liczba)
print(values)
print(add_next_date(dates))
