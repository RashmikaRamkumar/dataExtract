from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Path to ChromeDriver
driver_path = r"E:\chromedriver-win64\chromedriver.exe"

# Create a Service object
service = Service(driver_path)

# Initialize the Chrome WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Function to process a single website
def process_website(url, output_file):
    try:
        # Open the weather website
        driver.get(url)

        # Wait for the button to be present and click it twice to switch to 'm/s'
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-do='metric,wind']")))
        button.click()  # First click
        WebDriverWait(driver, 2).until(EC.staleness_of(button))  # Wait for the UI to update
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-do='metric,wind']")))
        button.click()  # Second click
        WebDriverWait(driver, 2).until(EC.staleness_of(button))  # Wait for the UI to update

        # Wait for the weather data to load after switching to 'm/s'
        weather_div = wait.until(EC.presence_of_element_located((By.ID, "plugin-detail")))

        # Extract the weather data
        weather_data = weather_div.text

        # Process the data into a tabular format
        rows = weather_data.split("\n")  # Split data into rows
        table_data = [row.split() for row in rows]  # Split each row into columns

        # Convert to a Pandas DataFrame
        df = pd.DataFrame(table_data)

        # Save the data to an Excel file
        df.to_excel(output_file, index=False, header=False)
        print(f"Weather data from {url} saved to {output_file}")

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

# List of websites to process
websites = [
    "https://www.windy.com/10.602/77.243?9.989,77.243,8",
    "https://www.windy.com/10.696/77.302?10.080,77.297,8",
    "https://www.windy.com/10.695/77.552?10.080,77.550,8",
    "https://www.windy.com/10.924/77.165?10.307,77.162,8",
    "https://www.windy.com/11.029/77.358?10.415,77.360,8",
    "https://www.windy.com/10.857/77.480?10.247,77.481,8",
    "https://www.windy.com/10.775/77.053?10.166,77.053,8",
    "https://www.windy.com/10.568/77.431?9.955,77.432,8",
    "https://www.windy.com/10.775/78.099?10.161,78.096,8"
]

# Process each website
for i, website in enumerate(websites, start=1):
    output_file = f"weather_data_{i}.xlsx"
    process_website(website, output_file)

# Close the browser after processing all websites
driver.quit()
