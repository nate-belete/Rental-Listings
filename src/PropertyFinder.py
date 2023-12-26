import pandas as pd
import numpy as np
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

class PropertyFinder:
    """
    A class for finding nearby properties within a specified radius of a given address based on latitude and longitude.
    """

    def __init__(self, df, address):
        """
        Initialize the PropertyFinder with a DataFrame containing properties' data and an address.
        
        Parameters:
        df (pd.DataFrame): A DataFrame with 'address', 'Longitude', and 'Latitude' columns.
        address (str): The address of the target property.
        """
        self.df = df
        self.target_lon, self.target_lat = self.property_longitude_latitude(address)

    @staticmethod
    def property_longitude_latitude(address):
        """
        Geocode an address to find its longitude and latitude using Nominatim.
        
        Parameters:
        address (str): The property's address.
        
        Returns:
        (float, float): A tuple containing the longitude and latitude of the property.
        """
        geolocator = Nominatim(user_agent="my-app")
        location = geolocator.geocode(address)
        if location:
            return location.longitude, location.latitude
        else:
            raise ValueError(f"Could not geocode address: {address}")

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the haversine distance between two geographic points.
        
        Parameters:
        lon1, lat1 (float): Longitude and latitude of the first point.
        lon2, lat2 (float): Longitude and latitude of the second point.
        
        Returns:
        float: Distance between the two points in kilometers.
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))

        # Radius of Earth in kilometers
        km = 6371 * c
        return km

    def find_within_radius(self, radius_miles):
        """
        Find properties within a certain radius from the target location.
        
        Parameters:
        radius_miles (float): Radius within which to search for properties, in miles.
        
        Returns:
        pd.DataFrame: DataFrame of nearby properties within the specified radius.
        """
        # Convert radius from miles to kilometers
        radius_km = radius_miles * 1.60934

        # Calculate distances from the target location using the haversine formula
        distances = self.df.apply(
            lambda row: self.haversine(self.target_lon, self.target_lat, row['Longitude'], row['Latitude']), axis=1
        )
        self.df['distance_km'] = distances

        # Filter and return properties within the specified radius
        properties_within_radius = self.df.loc[self.df['distance_km'] <= radius_km].copy()
        properties_within_radius.drop(columns='distance_km', inplace=True)
        
        return properties_within_radius, self.target_lon, self.target_lat,

    def add_clickable_links(self, df):
        """
        Add clickable links to property URLs in the DataFrame.
        
        Parameters:
        df (pd.DataFrame): A DataFrame with a 'URL' column to be converted to clickable links.
        
        Returns:
        pd.DataFrame: DataFrame with clickable URLs.
        """
        # Function to convert URLs to clickable links
        def make_clickable(url):
            return f'<a target="_blank" href="{url}">Link</a>'

        # Apply make_clickable to the 'URL' column
        df['Listing_URL'] = df['Listing_URL'].apply(make_clickable)
        return df