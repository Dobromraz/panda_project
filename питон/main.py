import pandas as pd
import matplotlib.pyplot as plt

# Загрузка файла
file_path = 'Space_Corrected.csv'
df = pd.read_csv(file_path)

# Очистка данных
df_cleaned = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])
df_cleaned.columns = [
    'Company_Name', 'Location', 'Launch_Date', 'Detail',
    'Rocket_Status', 'Rocket_Cost', 'Mission_Status'
]
df_cleaned['Launch_Date'] = pd.to_datetime(df_cleaned['Launch_Date'], errors='coerce', utc=True)
df_cleaned['Rocket_Cost'] = df_cleaned['Rocket_Cost'].astype(str).str.replace(',', '').str.strip()
df_cleaned['Rocket_Cost'] = pd.to_numeric(df_cleaned['Rocket_Cost'], errors='coerce')

# Создание вспомогательных столбцов
df_cleaned['Is_USA'] = df_cleaned['Location'].str.contains('USA', na=False)
df_cleaned['Year'] = df_cleaned['Launch_Date'].dt.year

print("\nПРОВЕРКА ГИПОТЕЗ С ГРАФИКАМИ:\n")

# 1. Китай vs США: у кого больше успехов
chinese_companies = ['CASC', 'ExPace', 'i-Space', 'LandSpace', 'OneSpace']
china = df_cleaned[df_cleaned['Company_Name'].isin(chinese_companies)]
usa = df_cleaned[df_cleaned['Is_USA']]

china_success_rate = (china['Mission_Status'] == 'Success').mean() * 100
usa_success_rate = (usa['Mission_Status'] == 'Success').mean() * 100

print("1. Процент успеха: Китай vs США")
print(f"   Китай: {china_success_rate:.2f}% успехов")
print(f"   США: {usa_success_rate:.2f}% успехов\n")

plt.figure(figsize=(8, 6))
plt.bar(['Китай', 'США'], [china_success_rate, usa_success_rate], color=['red', 'blue'])
plt.title('Процент успеха: Китай vs США')
plt.ylabel('Процент успехов (%)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 2. С годами стало больше удачных запусков
success_by_year = df_cleaned.groupby('Year')['Mission_Status'].apply(lambda x: (x == 'Success').mean() * 100)
print("2. Процент успешных запусков по годам:")
print(success_by_year.to_string())
print()

plt.figure(figsize=(10, 6))
success_by_year.plot(marker='o')
plt.title('Процент успешных запусков по годам')
plt.xlabel('Год')
plt.ylabel('Процент успехов (%)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. США делают более дорогие ракеты
usa_mean_cost = usa['Rocket_Cost'].mean()
non_usa = df_cleaned[~df_cleaned['Is_USA']]
non_usa_mean_cost = non_usa['Rocket_Cost'].mean()

print("3. Средняя стоимость ракет США vs Вне США")
print(f"   США: {usa_mean_cost:.2f} млн долларов")
print(f"   Вне США: {non_usa_mean_cost:.2f} млн долларов\n")

plt.figure(figsize=(8, 6))
plt.bar(['США', 'Вне США'], [usa_mean_cost, non_usa_mean_cost], color=['green', 'orange'])
plt.title('Средняя стоимость ракет: США vs Вне США')
plt.ylabel('Стоимость (млн долларов)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 4. У США процент успеха выше
print("4. Процент успеха запусков: США vs Вне США")
usa_success_rate = (usa['Mission_Status'] == 'Success').mean() * 100
non_usa_success_rate = (non_usa['Mission_Status'] == 'Success').mean() * 100
print(f"   США: {usa_success_rate:.2f}% успехов")
print(f"   Вне США: {non_usa_success_rate:.2f}% успехов\n")

plt.figure(figsize=(6, 6))
plt.pie([usa_success_rate, non_usa_success_rate], labels=['США', 'Вне США'], autopct='%1.1f%%', startangle=140)
plt.title('Процент успеха: США vs Вне США')
plt.axis('equal')
plt.tight_layout()
plt.show()

# 5. SpaceX делает запусков больше всех
company_launches = df_cleaned.groupby('Company_Name').size()
print("5. Количество запусков SpaceX и других компаний:")
print(company_launches.sort_values(ascending=False).head(10))
print()

plt.figure(figsize=(10, 6))
company_launches.sort_values(ascending=False).head(10).plot(kind='bar')
plt.title('Топ-10 компаний по количеству запусков')
plt.xlabel('Компания')
plt.ylabel('Количество запусков')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 6. Деньги влияют на успех запуска
successes = df_cleaned[df_cleaned['Mission_Status'] == 'Success']
failures = df_cleaned[df_cleaned['Mission_Status'] != 'Success']
mean_success_cost = successes['Rocket_Cost'].mean()
mean_failure_cost = failures['Rocket_Cost'].mean()

print("6. Средняя стоимость ракет: Успех vs Неудача")
print(f"   Успех: {mean_success_cost:.2f} млн долларов")
print(f"   Неудача: {mean_failure_cost:.2f} млн долларов\n")

plt.figure(figsize=(8, 6))
plt.bar(['Успех', 'Неудача'], [mean_success_cost, mean_failure_cost], color=['blue', 'red'])
plt.title('Средняя стоимость ракет: Успех vs Неудача')
plt.ylabel('Стоимость (млн долларов)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 7. Количество запусков по годам
launches_by_year = df_cleaned.groupby('Year').size()
print("7. Количество запусков по годам:")
print(launches_by_year.to_string())
print()

plt.figure(figsize=(10, 6))
launches_by_year.plot(marker='s', linestyle='-', color='purple')
plt.title('Динамика количества запусков по годам')
plt.xlabel('Год')
plt.ylabel('Количество запусков')
plt.grid(True)
plt.tight_layout()
plt.show()

# 8. Влияние времени года на успех запуска
seasons = {
    12: 'Зима', 1: 'Зима', 2: 'Зима',
    3: 'Весна', 4: 'Весна', 5: 'Весна',
    6: 'Лето', 7: 'Лето', 8: 'Лето',
    9: 'Осень', 10: 'Осень', 11: 'Осень'
}
df_cleaned['Season'] = df_cleaned['Launch_Date'].dt.month.map(seasons)

success_by_season = df_cleaned.groupby('Season')['Mission_Status'].apply(lambda x: (x == 'Success').mean() * 100)

print("8. Процент успехов по сезонам:")
print(success_by_season.to_string())
print()

plt.figure(figsize=(8, 6))
success_by_season = success_by_season.reindex(['Зима', 'Весна', 'Лето', 'Осень'])
success_by_season.plot(kind='bar', color=['skyblue', 'lightgreen', 'gold', 'orange'])
plt.title('Процент успешных запусков по сезонам')
plt.xlabel('Сезон')
plt.ylabel('Процент успехов (%)')
plt.ylim(0, 100)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
