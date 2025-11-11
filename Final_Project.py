import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the headers for the request to avoid blocking by the website
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# URL to scrape the data from
url = 'https://www.worldometers.info/coronavirus/'

# Send the HTTP request to fetch the page content
response = requests.get(url, headers=headers)

# Check if the response was successful
if response.status_code != 200:
    print("Failed to retrieve data from the provided link")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Try to extract the data from the table
try:
    # Find the main table with the country data
    tableData = soup.find("table", id="main_table_countries_today")
    tr = tableData.find("tbody").find_all("tr")

    # Get the headers from the table
    headers = [header.text.strip() for header in tableData.find("thead").find_all("th")]

    # Initialize a list to store the country data
    country_data = []
    
    # Loop through each row of the table
    for row in tr: 
        cols = row.find_all("td")
        # Clean the data and store it in the list
        cols = [col.text.strip() for col in cols]
        country_data.append(cols)
    
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(country_data, columns=headers)

except Exception as e:
    print(f"Error while reading the table: {e}")
    exit()

# Filter only the necessary columns: '#', 'country name', 'total cases', 'total deaths', 'total recovered', 'continent'
columns_to_include = ['Country,Other', 'TotalCases', 'TotalDeaths', 'TotalRecovered', 'Continent']
df_filtered = df[columns_to_include]

# Clean up column names to ensure no leading/trailing spaces
df_filtered.columns = df_filtered.columns.str.strip()

# Convert to numeric values for 'TotalCases', 'TotalDeaths', and 'TotalRecovered' columns
df_filtered['TotalCases'] = pd.to_numeric(df_filtered['TotalCases'].replace({',': ''}, regex=True), errors='coerce')
df_filtered['TotalDeaths'] = pd.to_numeric(df_filtered['TotalDeaths'].replace({',': ''}, regex=True), errors='coerce')
df_filtered['TotalRecovered'] = pd.to_numeric(df_filtered['TotalRecovered'].replace({',': ''}, regex=True), errors='coerce')

# Create a SQLite database and insert the filtered data
conn = sqlite3.connect("covid_data.db")
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''
CREATE TABLE IF NOT EXISTS covid_data (
    id INTEGER PRIMARY KEY,
    country_name TEXT,
    total_cases INTEGER,
    total_deaths INTEGER,
    total_recovered INTEGER,
    continent TEXT
)
''')

# Insert the data into the table
for index, row in df_filtered.iterrows():
    cursor.execute('''
    INSERT INTO covid_data (country_name, total_cases, total_deaths, total_recovered, continent)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['Country,Other'], row['TotalCases'], row['TotalDeaths'], row['TotalRecovered'], row['Continent']))


df_north_america = df_filtered[df_filtered['Continent'] == 'North America']
# Create a new table for North America countries
cursor.execute('''
CREATE TABLE IF NOT EXISTS covid_data_north_america (
    id INTEGER PRIMARY KEY,
    country_name TEXT,
    total_cases INTEGER,
    total_deaths INTEGER,
    total_recovered INTEGER,
    continent TEXT
)
''')

# Insert the filtered North America data into the new table
for index, row in df_north_america.iterrows():
    cursor.execute('''
    INSERT INTO covid_data_north_america (country_name, total_cases, total_deaths, total_recovered, continent)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['Country,Other'], row['TotalCases'], row['TotalDeaths'], row['TotalRecovered'], row['Continent']))



# Update the main table (covid_data) to replace NULL values with 0
cursor.execute('''
UPDATE covid_data
SET total_cases = COALESCE(total_cases, 0),
    total_deaths = COALESCE(total_deaths, 0),
    total_recovered = COALESCE(total_recovered, 0)
''')

# Update the North America table (covid_data_north_america) to replace NULL values with 0
cursor.execute('''
UPDATE covid_data_north_america
SET total_cases = COALESCE(total_cases, 0),
    total_deaths = COALESCE(total_deaths, 0),
    total_recovered = COALESCE(total_recovered, 0)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Save the cleaned data to a CSV file
df_filtered.to_csv("covid_stats_filtered.csv", index=False)
print("Data has been successfully inserted into the SQLite database!")

df = pd.read_csv("covid_stats_filtered.csv")
print(df)

df['TotalCases'] = pd.to_numeric(df['TotalCases'], errors='coerce')
# Calculating statistics of the 'TotalCases' column using numpy
mean_total_cases = int(np.mean(df['TotalCases']))
variance_total_cases = int(np.var(df['TotalCases']))
std_total_cases = int(np.std(df['TotalCases']))

print(f"The mean of Total Cases is: {mean_total_cases:,}")
print(f"The variance of Total Cases is: {variance_total_cases:,}")
print(f"The standard deviation of Total Cases is: {std_total_cases:,}")


conn = sqlite3.connect("covid_data.db")
# Query to fetch data from the 'covid_data_north_america' table
query_na = "SELECT * FROM covid_data_north_america"
# Load the data into a pandas DataFrame
df_north_america = pd.read_sql_query(query_na, conn)
north_america = (df_north_america.loc[0])
north_america_total_cases = north_america['total_cases']
north_america_total_deaths = north_america['total_deaths'] 
north_america_morality_rate = north_america_total_deaths/north_america_total_cases
print(f"The moratality rate in North America was {north_america_morality_rate:%}")
global_ = df.loc[7]
global_total_cases = global_['TotalCases']
global_total_deaths = global_['TotalDeaths'] 
global_morality_rate = global_total_deaths/global_total_cases
print(f"The moratality rate globally was {global_morality_rate:%}")


y = np.array([global_total_cases, global_total_deaths])
mylabels = ["Global cases", "Global deaths"]
plt.pie(y, labels = mylabels)
plt.show()

x = np.array(["North American Cases", "Global Cases"])
y = np.array([north_america_total_cases, global_total_cases])

plt.bar(x, y)
plt.ylabel = "North American v. Global"
plt.xlabel = "Number of cases"
plt.show()

x = np.array([ "North American Deaths", "Global Deaths"])
y = np.array([ north_america_total_deaths, global_total_deaths])

plt.bar(x, y)
plt.ylabel = "North American v. Global"
plt.xlabel = "Number of deaths"
plt.show()