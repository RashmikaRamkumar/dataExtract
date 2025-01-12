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

#first approach
# try:
#     # Open the weather website
#     driver.get(r"https://www.windy.com/9.926/78.114?14.158,78.992,5")

#     # Wait for the weather data to load
#     wait = WebDriverWait(driver, 10)
#     weather_div = wait.until(EC.presence_of_element_located((By.ID, "plugin-detail")))

#     # Extract and print the weather data
#     print("Weather Data:")
#     print(weather_div.text)

# finally:
#     # Close the browser
#     driver.quit()


#second approach
try:
    # Open the weather website
    driver.get(r"https://www.windy.com/10.602/77.243?9.989,77.243,8")
    

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

    # Extract and print the weather data
    print("Weather Data in m/s:")
    print(weather_div.text)
    # Process the data into a tabular format
    weather_data = weather_div.text

    rows = weather_data.split("\n")  # Split data into rows
    table_data = [row.split() for row in rows]  # Split each row into columns

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(table_data)

    # Save the data to an Excel file
    excel_file = "weather_data.xlsx"
    df.to_excel(excel_file, index=False, header=False)
    print(f"Weather data saved to {excel_file}")


finally:
    # Close the browser
    driver.quit()


