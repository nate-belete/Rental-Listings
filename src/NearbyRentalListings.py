import pandas as pd

class NearbyRentalListings:
    def __init__(self, data_file_path, current_rent):
        """
        Initialize the NearbyRentalListings object with the path to the data file
        and the user's current rent.
        
        Args:
        - data_file_path (str): Path to the CSV file containing rental data.
        - current_rent (float): The user's current rent.
        """
        self.data_file_path = data_file_path
        self.current_rent = current_rent
        self.df = pd.read_csv(data_file_path)

    def get_nearby_properties(self, zipcode, bedroom, query_date_prior, query_date):
        """
        Fetch and return listings for rentals filtered by ZIP code, number of bedrooms,
        and query date range.
        
        Args:
        - zipcode (str): The ZIP code to filter the rental data.
        - bedroom (int): The number of bedrooms to filter the rental data.
        - query_date_prior (str): The start date for the query in 'YYYY-MM-DD' format.
        - query_date (str): The end date for the query in 'YYYY-MM-DD' format.
        
        Returns:
        - pd.DataFrame: A DataFrame containing the nearby rental properties.
        """
        filtered_df = self.df[
            (self.df['Query_Zip_Code'].astype(str) == zipcode) &
            (self.df['Bedroom'] == bedroom) &
            (self.df['Query_Date'] >= query_date_prior) &
            (self.df['Query_Date'] <= query_date)
        ]
        columns_of_interest = ['Listing_URL', 'Address', 'Bedroom', 'Bathroom','Sqft','Price' ]
        return filtered_df[columns_of_interest].dropna().drop_duplicates().sort_values('Price', ascending = False)

    @staticmethod
    def display_nearby_properties(df):
        """
        Convert 'Listing_URL' column in the dataframe to clickable HTML links and display in streamlit.
        
        Args:
        - df (pd.DataFrame): DataFrame containing rental properties with 'Listing_URL' column.
        
        Returns:
        - pd.DataFrame: DataFrame with the 'Listing_URL' column formatted as clickable links.
        """
        def make_clickable(url):
            # Function to convert a URL into a clickable HTML link
            return f'<a href="{url}" target="_blank">View Listing</a>'

        df['Listing_URL'] = df['Listing_URL'].apply(make_clickable)
        return df
