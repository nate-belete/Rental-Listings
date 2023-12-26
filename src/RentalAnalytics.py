import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st

class RentalAnalytics:
    def __init__(self, data_file_path):
        """
        Initialize the RentalAnalytics object with the path to the data file
        and the user's current rent.
        
        Args:
        - data_file_path (str): Path to the CSV file containing rental data.
        - current_rent (float): The user's current rent.
        """
        self.data_file_path = data_file_path
        self.df = pd.read_csv(data_file_path)

    def clean_data(self, df):
        """
        Clean the rental data by converting 'Price' and 'Sqft' to numeric
        and dropping any NaNs.
        
        Args:
        - df (pd.DataFrame): DataFrame containing rental properties.
        
        Returns:
        - pd.DataFrame: Cleaned DataFrame with numeric 'Price' and 'Sqft'.
        """
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df['Sqft'] = pd.to_numeric(df['Sqft'], errors='coerce')
        df = df.dropna(subset=['Price', 'Sqft'])
        return df

    def plot_price_with_regression(self, zipcode, bedroom, query_date_prior, query_date):
        """
        Create a scatter plot with regression line showing the relationship
        between 'Price' and 'Sqft' for the filtered DataFrame.
        
        Args:
        - df_filtered (pd.DataFrame): DataFrame containing rental properties.
        """
        cleaned_df = self.df[
                            (self.df['Query_Zip_Code'].astype(str) == zipcode) &
                            (self.df['Bedroom'] == bedroom) 
                            # (self.df['Query_Date'] >= query_date_prior) &
                            # (self.df['Query_Date'] <= query_date)
                            ].copy()

        plt.figure(figsize=(10, 5))
        sns.regplot(x='Sqft', 
                    y='Price', 
                    data=cleaned_df, 
                    scatter_kws={'alpha': 0.5})
        plt.title('Price vs. Square Footage with Linear Regression Line')
        plt.xlabel('Square Footage')
        plt.ylabel('Price')
        plt.grid(True)
        plt.show()

    def plot_price_by_bedroom_boxplot(self, zipcode, bedroom, query_date_prior, query_date):
        """
        Create a box plot segmented by the number of bedrooms showing the
        distribution of rental prices for the filtered DataFrame.
        
        Args:
        - df_filtered (pd.DataFrame): DataFrame containing rental properties.
        """
        cleaned_df = self.df[
                            (self.df['Query_Zip_Code'].astype(str) == zipcode) &
                            (self.df['Query_Date'] >= query_date_prior) &
                            (self.df['Query_Date'] <= query_date)
                            ].copy()

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Bedroom', y='Price', data=cleaned_df)
        plt.title('Rental Prices by Number of Bedrooms')
        plt.xlabel('Number of Bedrooms')
        plt.ylabel('Price')
        plt.grid(True)
        plt.show()