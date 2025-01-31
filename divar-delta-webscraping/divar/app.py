from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://divar.ir/s/tehran/buy-apartment/chitgar?business-type=personal'

try:
    page = requests.get(url)
    page.raise_for_status()  # Raise an error for bad status codes
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
    exit()

soup = BeautifulSoup(page.text, 'html.parser')
searchInfo = soup.find_all('div', class_='widget-col-d2306')

data = []  # For adding data

for x in searchInfo:
    try:
        # Extract link
        a_tag = x.find('a')
        if a_tag and 'href' in a_tag.attrs:
            ATags = a_tag['href']
            ATags = "https://divar.ir" + ATags if not ATags.startswith('http') else ATags
        else:
            ATags = "N/A"

        # Extract title
        title_tag = x.find('h2', class_="kt-post-card__title")
        Title = title_tag.text.strip() if title_tag else "N/A"

        # Extract price
        price_tag = x.find('div', class_='kt-post-card__description')
        Price = price_tag.text.strip().replace(' ', '') if price_tag else "N/A"

        # Extract additional info
        info_tag = x.find('span', class_='kt-post-card__red-text')
        Info = info_tag.text.strip() if info_tag else " "

        # Extract location
        location_tag = x.find('span', class_='kt-post-card__bottom-description kt-text-truncate')
        location = location_tag.text.strip() if location_tag else "N/A"

        # Create a dictionary for each entry
        entry = {
            'Links': ATags,
            'Title': Title,
            'Info': Info,
            'Price': Price,
            'Location': location,
        }

        data.append(entry)
    except Exception as e:
        print(f"Error processing a listing: {e}")

# Convert the list of dictionaries to a DataFrame and save to Excel
if data:
    df = pd.DataFrame(data)
    df.to_excel('data.xlsx', index=False)
    print("Data saved to data.xlsx")
else:
    print("No data found.")