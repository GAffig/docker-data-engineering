#parameterized script example for pipeline testing
import sys

import pandas as pd

print('arguments:', sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({"Day": [1, 2], "num_passengers": [3, 4], "month": [month, month]})
print(df.head())

df.to_parquet(f"output_month_{month}.parquet ")
print(f'hello pipeline, month {month}')