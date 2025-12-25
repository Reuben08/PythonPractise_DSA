# test_widgets.py

import pandas as pd
from datetime import datetime
from pages.reusable_widgets import get_min_max_dates

def test_get_min_max_dates():
    # Sample dataframe
    data = {
        'Date': ['2023-01-01', '2023-01-05', '2023-01-10'],
        'Value': [10, 20, 30]
    }
    df = pd.DataFrame(data)

    min_date, max_date = get_min_max_dates(df)

    assert isinstance(min_date, datetime)
    assert isinstance(max_date, datetime)
    assert min_date == datetime(2023, 1, 1)
    assert max_date == datetime(2023, 1, 10)