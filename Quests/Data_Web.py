import requests
import datetime
import pandas as pd

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

# Data sprzed 10 lat
ten_years_ago = datetime.datetime.now() - datetime.timedelta(days=10*365)
ten_years_ago_str = ten_years_ago.strftime("%Y-%m-%dT00:00:00Z")

query = f"""
SELECT ?company ?companyLabel ?revenue ?oldName ?lastChangeDate WHERE {{

  {{
    SELECT ?company (MAX(?startDate) AS ?lastChangeDate) WHERE {{
      ?company wdt:P31 wd:Q4830453.
      ?company p:P1448 ?nameStatement.
      ?nameStatement ps:P1448 ?oldName.
      ?nameStatement pq:P580 ?startDate.
      FILTER(?startDate >= "{ten_years_ago_str}"^^xsd:dateTime)
    }}
    GROUP BY ?company
  }}

  ?company p:P1448 ?nameStatement2.
  ?nameStatement2 ps:P1448 ?oldName.
  ?nameStatement2 pq:P580 ?lastChangeDate.

  # PRZYCHÓD
  ?company wdt:P2139 ?revenue.

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
ORDER BY DESC(?revenue)
LIMIT 40
"""

headers = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "CompanyNameChangeBot/5.0"
}

response = requests.get(
    WIKIDATA_ENDPOINT,
    params={"query": query},
    headers=headers
)

data = response.json()
results = data["results"]["bindings"]

df = pd.DataFrame([
    {
        "Company": r["companyLabel"]["value"],
        "Previous Name": r["oldName"]["value"],
        "Last Change Date": r["lastChangeDate"]["value"],
        "Revenue (raw)": float(r["revenue"]["value"])
    }
    for r in results
])

# dodatkowe sortowanie w Pythonie (bezpiecznik)
df = df.sort_values(by="Revenue (raw)", ascending=False).head(40)
df=df.drop_duplicates(subset=["Revenue (raw)"], keep="first")
print(df.columns)