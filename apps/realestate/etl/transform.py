import pandas as pd

def load_data():

    df = pd.read_csv(
        "apps/realestate/data/gotham_urban_projects.csv"
    )

    # Normalizar nombres
    df.columns = df.columns.str.lower().str.strip()

    # Normalizar estados
    df["estado"] = df["estado"].astype(str).str.strip()

    return df