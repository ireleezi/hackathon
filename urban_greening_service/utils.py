from config import config
import pandas as pd
import requests
from io import StringIO

def fetch_onidata() -> pd.DataFrame:
    try:
        resp = requests.get(config.ONI_DATASET_URL)
        resp.raise_for_status()
        data = StringIO(resp.text)
        return pd.read_csv(data, skipinitialspace=True, quotechar='"')
    except Exception as e:
        print(f"Error fetching ONI Data: {e}")
        return None
    
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    #use OpenAI to map out areas where trees can be planted
    #omit areas with trees and infrastructure
    #input council area as parameter to keep response size manageable
    return df['TREELOCATIONX'].to_dict()
