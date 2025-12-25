import pandas as pd
import numpy as np

# csv load
df = pd.read_csv("/Users/reubenharuray/Downloads/HIT_DATA.csv")

# add row num
df["original_row_num"] = np.arange(1, len(df) + 1)

# define
evar_columns = [f"POST_EVAR{i}" for i in range(169, 251)]
existing_evar_columns = [col for col in evar_columns if col in df.columns]

# clean
df["POST_PRODUCT_LIST"] = df["POST_PRODUCT_LIST"].fillna("").astype(str)

# Explode POST_PRODUCT_LIST
df["Exploded_POST_PRODUCT_LIST"] = df["POST_PRODUCT_LIST"].apply(lambda x: x.split(",") if x else [])
df_exploded = df.explode("Exploded_POST_PRODUCT_LIST").reset_index(drop=True)

# product  string parser
def process_raw_string(row):
    raw_string = row["Exploded_POST_PRODUCT_LIST"]
    event_list = row.get("POST_EVENT_LIST", "")
    evar_values = [str(row.get(col, '0')) if pd.notna(row.get(col)) else '0' for col in existing_evar_columns]

    parts = raw_string.split(';')
    category = parts[0] if len(parts) > 0 else '0'
    name = parts[1] if len(parts) > 1 else '0'
    quantity = parts[2] if len(parts) > 2 and parts[2] else '0'
    price = parts[3] if len(parts) > 3 and parts[3] else '0'
    events = parts[4] if len(parts) > 4 else ''
    evars = parts[5] if len(parts) > 5 else ''

    events_list = [e for e in events.split('|') if '=' in e and e.split('=')[1] != '::hash::0']
    evar_list = [e for e in evars.split('|') if '=' in e and e.split('=')[1] != '::hash::0']

    events_values = [e.split('=')[1] for e in events_list]
    evar_values_list = [e.split('=')[1] for e in evar_list]

    evar_columns_with_values = [col for col, val in zip(existing_evar_columns, evar_values) if val != '0']
    evars_values_hit = [val for val in evar_values if val != '0']

    return pd.Series({
        "Category": category,
        "Name": name,
        "Quantity": quantity,
        "Price": price,
        "EventsList": events_list,
        "EvarList": evar_list,
        "EventList": event_list,
        "EvarColumnsWithValues": evar_columns_with_values,
        "EventsValues": events_values,
        "EvarValuesList": evar_values_list,
        "EvarsValuesHit": evars_values_hit
    })

# parsing
processed_df = df_exploded.apply(process_raw_string, axis=1)
df_final = pd.concat([df_exploded, processed_df], axis=1)

# iterate and print
for i, row in df_final.iterrows():
    row_num = row["original_row_num"]

    print(f"CategoryOfProduct_{i+1}_Row_{row_num}: {row['Category']}")
    print(f"NameOfProduct_{i+1}_Row_{row_num}: {row['Name']}")
    print(f"QuantityOfProduct_{i+1}_Row_{row_num}: {row['Quantity']}")
    print(f"PriceOfProduct_{i+1}_Row_{row_num}: {row['Price']}")
    print(f"EventsOfProduct_{i+1}_Row_{row_num}: {'|'.join(row['EventsList'])}")
    print(f"EvarsOfProduct_{i+1}_Row_{row_num}: {'-'.join(row['EvarList'])}")
    print(f"Values_Product_{i+1}_Row_{row_num}: {row['Category']}-{row['Name']}-{row['Quantity']}-{row['Price']}-{'-'.join(row['EventsValues'] + row['EvarValuesList'])}\n")

    # Events and keys
    if pd.notna(row['EventList']):
        event_values_of_hit = [e.split('=')[1] if '=' in e else '0' for e in row['EventList'].split(',')]
        print(f"EventsOfHIT_Row_{row_num}: {row['EventList']}")
        print(f"EventValuesOfHIT_Row_{row_num}: {'-'.join(event_values_of_hit)}")
    else:
        print(f"EventsOfHIT_Row_{row_num}: ")
        print(f"EventValuesOfHIT_Row_{row_num}: 0-0-0")

    print(f"EvarsOfHIT_Row_{row_num}: {'-'.join(row['EvarColumnsWithValues'])}")
    print(f"Evars_Values_HIT_Row_{row_num}: {'-'.join(row['EvarsValuesHit'])}")
    print(f"KeyOfHIT_Row_{row_num}: {row.get('hitid_high', 'NA')}-{row.get('hitid_low', 'NA')}-{row.get('visit_num', 'NA')}-{row.get('visit_page_num', 'NA')}")
    print(f"KeyOfVISIT_Row_{row_num}: {row.get('post_visid_high', 'NA')}-{row.get('post_visid_low', 'NA')}")
    print(f"KeyOfVISIT_REFERRER_Row_{row_num}: {row.get('VISIT_REFERRER', '')}")
    print(f"KeyOfVISIT_REFERRER_TYPE_Row_{row_num}: {row.get('VISIT_REF_TYPE', '')}")
    print(f"KeyOfCAMPAIGN_Row_{row_num}: {row.get('POST_CAMPAIGN', '')}")
    print(f"KeyOfMOBILE_APP_VERSION_Row_{row_num}: {row.get('POST_MOBILEAPPID', '')}")
    print(f"KeyOfMOBILE_Row_{row_num}: {row.get('MOBILE_ID', '')}")
    print(f"KeyOfVISITOR_Row_{row_num}: {str(row.get('post_visid_high', ''))}{str(row.get('post_visid_low', ''))}")
    print(f"KeyOfBROWSER_Row_{row_num}: {row.get('BROWSER', '')}")
    print(f"KeyOfCLOUD_VISITOR_Row_{row_num}: {row.get('MCVISID', '')}")
    print(f"KeyOfLOCATION_Row_{row_num}: {row.get('GEO_CITY', '')}-{row.get('GEO_COUNTRY', '')}-{row.get('GEO_DMA', '')}-{row.get('GEO_REGION', '')}")
    print(f"KeyOfSEARCHENGINE_Row_{row_num}: {row.get('POST_SEARCH_ENGINE', '')}")
    print("\n\n")