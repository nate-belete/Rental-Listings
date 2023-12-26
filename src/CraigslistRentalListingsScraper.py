import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime

class CraigslistRentalListingsScraper:
    def __init__(self, zipcode, miles, bedrooms, sample_size):
        self.zipcode = zipcode
        self.miles = miles
        self.bedrooms = bedrooms
        self.sample_size = sample_size
        self.query_date = datetime.now().strftime("%Y-%m-%d")
        self.base_url = f"https://sfbay.craigslist.org/search/apa?max_bedrooms={self.bedrooms}&min_bedrooms={self.bedrooms}&postal={self.zipcode}&search_distance={self.miles}"

        self.listings_data = []
    
    def scrape_listings(self):
        """
        Start the scraping process for Craigslist listings.
        """
        response = requests.get(self.base_url)

        if response.status_code == 200:
            html_soup = BeautifulSoup(response.text, 'html.parser')
            listings = html_soup.find_all('li')

            # Extracting URLs from the listings
            listing_urls = [listing.find('a')['href'] for listing in listings if listing.find('a')]
            listing_urls = list(set(listing_urls))  # Remove duplicates

            for listing_url in listing_urls[:self.sample_size]:
                self.scrape_listing(listing_url)
                time.sleep(random.randint(2, 5))  # Pause between requests

            print(f"Total records: {len(self.listings_data)}")

            return self.listings_data
        else:
            print("Failed to retrieve listings.")
            return []

    def scrape_listing(self, url):
        """
        Scrape data from an individual listing page.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            listing_data = self.extract_listing_data(soup, url)
            self.listings_data.append(listing_data)

    def extract_listing_data(self, soup, url):
        """
        Extract the relevant info from the listing's BeautifulSoup object.
        """
        price = self.extract_text(soup.find('span', class_='price'), '').replace('$','').replace(",",'')
        address = self.extract_text(soup.find('h2', class_='street-address'), 'Unknown')
        latitude = self.extract_attribute(soup.find('div', class_='viewposting'), 'data-latitude', np.nan)
        longitude = self.extract_attribute(soup.find('div', class_='viewposting'), 'data-longitude', np.nan)
        
        bedrooms, bathrooms, sqft = self.extract_housing_info(soup.find_all('span', class_='shared-line-bubble'))
        
        return {
            "Listing_URL": url,
            "Address": address,
            "Price": price,
            "Bedroom": bedrooms,
            "Bathroom": bathrooms,
            "Sqft": sqft,
            "Query_Zip_Code": str(self.zipcode),
            "Query_Miles": self.miles,
            "Longitude": longitude,
            "Latitude": latitude,
            "Query_Date": self.query_date
        }
    
    @staticmethod
    def extract_text(element, default):
        """
        Extract text from a BeautifulSoup element with handling for missing elements.
        """
        return element.text.strip() if element else default

    @staticmethod
    def extract_attribute(element, attribute, default):
        """
        Extract attribute value from a BeautifulSoup element with handling for missing elements.
        """
        return element[attribute] if element else default

    @staticmethod
    def extract_housing_info(elements):
        """
        Extract housing information (bedrooms, bathrooms, square footage) from listing.
        """
        bedrooms = bathrooms = sqft = np.nan

        for element in elements:
            text = element.text.split('/')
            for item in text:
                if 'BR' in item:
                    bedrooms = item.split('BR')[0].strip()
                elif 'Ba' in item:
                    bathrooms = item.split('Ba')[0].strip()
                elif 'ft2' in item:
                    sqft = item.split('ft2')[0].strip()

        return bedrooms, bathrooms, sqft

    def save_to_csv(self, filename):
        """
        Save the scraped data to a CSV file.
        """
        df = pd.DataFrame(self.listings_data)

        # Cleaning and formatting the DataFrame
        numeric_cols = ['Price', 'Bedroom', 'Bathroom']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['Query_Zip_Code'] = df['Query_Zip_Code'].astype(str)
        df['Query_Miles'] = df['Query_Miles'].astype(float)
        df.to_csv(filename, index=False, mode='a', header=False)  # Appending to an existing CSV
        print(f"Cleaned dataset saved to {filename}: {df.shape}")
