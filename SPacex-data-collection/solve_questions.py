import requests
import pandas as pd
import datetime
import numpy as np
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)

# --- API Section ---
print("Fetching API data...")
url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(url)
data = pd.json_normalize(response.json())

# Q1
print("\n--- Q1 ---")
first_static_fire = data.loc[0, 'static_fire_date_utc']
print(f"First row static_fire_date_utc: {first_static_fire}")
if first_static_fire:
    print(f"Year: {pd.to_datetime(first_static_fire).year}")

# Filtering logic from notebook
print("\nApplying filters...")
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])
data['date'] = pd.to_datetime(data['date_utc']).dt.date
data = data[data['date'] <= datetime.date(2020, 11, 13)]

print(f"Data shape after filtering: {data.shape}")

# Q2
print("\n--- Q2 ---")
# Map rocket IDs to names
rocket_ids = data['rocket'].unique()
rocket_map = {}
for rid in rocket_ids:
    r_url = f"https://api.spacexdata.com/v4/rockets/{rid}"
    r_resp = requests.get(r_url).json()
    rocket_map[rid] = r_resp['name']

data['BoosterVersion'] = data['rocket'].map(rocket_map)
print("Rocket counts:")
print(data['BoosterVersion'].value_counts())

data_falcon9 = data[data['BoosterVersion'] != 'Falcon 1']
print(f"Falcon 9 count (after removing Falcon 1): {len(data_falcon9)}")

# Q3
print("\n--- Q3 ---")
# Check LandingPad in cores
# The notebook uses getCoreData to populate LandingPad list.
# It likely uses the 'landingpad' field from the core object.
# In the launches response, 'cores' is a list of dicts. We extracted the first dict.
# Let's see if 'landingpad' is in that dict.
sample_core = data.iloc[0]['cores']
print(f"Sample core dict keys: {sample_core.keys()}")

if 'landingpad' in sample_core:
    # Count missing values in 'landingpad' for Falcon 9 data
    # Note: The notebook creates a new dataframe `data_falcon9` and then checks missing values.
    # The `LandingPad` column in the new dataframe comes from the `LandingPad` list.
    # The `LandingPad` list is populated by `getCoreData`.
    # If `getCoreData` just takes `core['landingpad']`, then we can use that.
    
    # Let's extract landingpad column
    data_falcon9 = data_falcon9.copy()
    # The key is 'landpad' based on the output
    data_falcon9['LandingPad'] = data_falcon9['cores'].apply(lambda x: x.get('landpad'))
    
    missing_count = data_falcon9['LandingPad'].isnull().sum()
    print(f"Missing LandingPad count: {missing_count}")
    print("Value counts for LandingPad:")
    print(data_falcon9['LandingPad'].value_counts(dropna=False))
else:
    # Check for 'landpad'
    if 'landpad' in sample_core:
        data_falcon9 = data_falcon9.copy()
        data_falcon9['LandingPad'] = data_falcon9['cores'].apply(lambda x: x.get('landpad'))
        missing_count = data_falcon9['LandingPad'].isnull().sum()
        print(f"Missing LandingPad count (using 'landpad'): {missing_count}")
    else:
        print("'landingpad' and 'landpad' not in core dict.")

# --- Webscraping Section ---
print("\n--- Q4 ---")
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}
response_wiki = requests.get(static_url, headers=headers)
soup = BeautifulSoup(response_wiki.text, 'html.parser')
print(f"soup.title: {soup.title}")
