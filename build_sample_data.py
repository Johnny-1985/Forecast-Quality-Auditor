import csv
import random

random.seed(42)

months = []
for year in (2024, 2025):
    for m in range(1, 13):
        months.append(f"{year}-{m:02d}")

rows = []
base = 1000
for i, month in enumerate(months):
    trend = base + i * 12
    seasonal = 80 * (1 if (i % 12) in (10, 11, 0) else (0.3 if (i % 12) in (5, 6, 7) else 0))
    actual = trend + seasonal + random.gauss(0, 25)

    # Forecast: generally tracks actual with noise, mild systematic over-forecast bias,
    # and a couple of deliberately planted large misses (outliers) to demonstrate detection.
    forecast = actual * 1.04 + random.gauss(0, 35)
    if month in ("2024-11", "2025-03"):  # planted outliers
        forecast = actual * 1.45
    if month == "2025-07":
        forecast = actual * 0.6

    rows.append({
        "Period": month,
        "Forecast_Units": round(forecast),
        "Actual_Units": round(actual),
    })

with open("/home/claude/sample_forecast_actual.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Period", "Forecast_Units", "Actual_Units"])
    writer.writeheader()
    writer.writerows(rows)

print("Sample CSV written:", len(rows), "rows")
