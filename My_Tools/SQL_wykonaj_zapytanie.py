"""
w celu szybszego działania python-sql
przygotowałem funkcję gdzie mam już nastart przygotowane parametry SQL.
Teraz mogę odwołać się do funkcji wstawiając
1 zmienną=zapytanie i alternatywnie następne jako zmienne/tablice których używam w zapytaniu
"""
def SQL_Scheme(*args):
    import pyodbc
    server = r'LAPTOP-K210UGHT\MSSQLSERVER01'
    database = 'Git_Projects'

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()

    if len(args) == 1:
        cursor.execute(args[0])
        print("wykonano polecenie bez zmiennych"+args[0])
    elif len(args) >= 2:
        cursor.fast_executemany = True
        cursor.executemany(*args)
        print("wykonano polecenie ze zmiennymi"+args[0])
    conn.commit()