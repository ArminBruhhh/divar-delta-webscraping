from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://delta.ir/tehran/buy-apartment/region-21-22-chitgar?id=OIJHqFWOBuo=&orderBy=0&yearBuildId=0&AdvertiserTypeId=1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
searchInfo = soup.find_all('div', class_='search-results-info-boxes')

data = []  # For adding data

for x in searchInfo:
    ATags = x.find('a').get('href')
    Title = x.find('h2').text.strip()
    Info = x.find('div', class_='search-list-item clearfix')
    
    PInfo = []
    for i in Info.find_all('span', class_='search-list-info'):
        Info1 = i.text.strip()  # Collecting information from spans
        PInfo.append(Info1)

    Price = x.find('div', class_='search-list-price').text.strip().replace(' ', '')
    MPrice = x.find('div', class_='search-list-price price-metter').text.strip().replace(' ', '')
    location = x.find('div', class_='search-list-location').text.strip().replace(' ', '')

    # Create a dictionary for each entry with separate columns for each description
    entry = {
        'Links' : ATags,
        'Title': Title,
        'Description1': PInfo[0] if len(PInfo) > 0 else None,
        'Description2': PInfo[1] if len(PInfo) > 1 else None,
        'Description3': PInfo[2] if len(PInfo) > 2 else None,
        'MPrice': MPrice,
        'Price': Price,
        'Location': location,
    }
    
    data.append(entry)

# Convert the list of dictionaries to a DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel('data.xlsx', index=False)
