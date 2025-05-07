import re

data = ["1450XV век", "850VIV", "1870-е"]
years = []

for s in data:
    # Ищем 1-4 цифры в начале строки
    match = re.match(r'^(\d{1,4})', s)
    if match:
        years.append(int(match.group(1)))

print(years)  # [1450, 850, 1870]