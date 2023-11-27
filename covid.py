import time
import warnings

import pandas as pd

warnings.filterwarnings("ignore")

print("preparing data...")
df = pd.read_excel("covid_cases.xlsx")

df = df.set_index("Date_reported")
df = df.asfreq("D")

df = df.New_cases

y_train = df.loc[:"2022-12-31 23:59:00"]
y_val = df.loc["2022-12-31 23:59:00":"2023-08-31 23:59:00"]
y_train_val = df.loc[:"2023-08-31 23:59:00"]
y_test = df.loc["2023-08-31 23:59:00":]

y_train = y_train.asfreq("D")
y_val = y_val.asfreq("D")
y_train_val = y_train_val.asfreq("D")
y_test = y_test.asfreq("D")


print("starting SARIMAX...")
from itertools import product

from skforecast.Sarimax import Sarimax
from sklearn.metrics import mean_squared_error

order = list(product(range(12), range(12), range(12)))
seasonal_order = list(product(range(2, 4), range(2, 4), range(2, 4), range(2, 4)))

stats = list(product(order, seasonal_order))
best, mn = None, float("inf")
print(f"{len(stats)} models to check...")


errors = 0
for i, (ord, sea_ord) in enumerate(stats):
    print(f"Model #: {i+1}")
    print(f"Order: {ord}")
    print(f"Seasonal order: {sea_ord}")

    t = time.perf_counter()
    try:
        model = Sarimax(ord, sea_ord)
        model.fit(y_train)
        y_pred = model.predict(y_val.size)

    except Exception as e:
        print(f"Error: {e}", end="\n\n")
        errors += 1
        continue

    mse = mean_squared_error(y_val, y_pred)

    print(f"MSE: {mse:_.2f}")
    if mse < mn:
        print(f"New Best: {ord=} {sea_ord=}")
        best = (ord, sea_ord)
        mn = mse

    print(f"{time.perf_counter() - t:.2}s")
    print(f"Curr Best: {best} MSE: {mn:_.2f}")
    print()


print(f"BEST MODEL: {best}")
print(f"BEST MODEL: {mn:_.2f}")
print(f"Errors: {errors}/{len(stats)}")
