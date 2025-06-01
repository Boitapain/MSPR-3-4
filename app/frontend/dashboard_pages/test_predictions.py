"""Unit tests for verifying country code and CSV Id consistency."""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def test_country_code_matches_csv_id():
    """Test que le code Cuntry correspond à l'Id dans data_etl_output.csv."""
    try:
        df = pd.read_csv("../data_etl_output.csv")
    except FileNotFoundError:
        assert False, "Ohlala Le fichier ../data_etl_output.csv est introuvable."

    required_columns = ['Country', 'Id']
    for col in required_columns:
        assert col in df.columns, f"La colonne '{col}' est manquante dans le fichier CSV."

    countries = sorted(df['Country'].unique())
    le = LabelEncoder()
    le.fit(df['Country'])
    country_to_code = {
        country: int(code)
        for country, code in zip(le.classes_, le.transform(le.classes_))
    }
    country_id_map = (
        df.drop_duplicates(subset=["Country"])[["Country", "Id"]]
        .set_index("Country")["Id"].to_dict()
    )

    for country in countries:
        assert country_to_code[country] == country_id_map[country] - 1, (
            f"{country}: code={country_to_code[country]}, id={country_id_map[country]}"
        )
