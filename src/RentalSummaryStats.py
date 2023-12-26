import pandas as pd
import streamlit as st

class RentalSummaryStats:
    def __init__(self, data_file_path, current_rent):
        """
        Initialize the RentalSummaryStats object with the path to the data file
        and the user's current rent.
        
        Args:
        - data_file_path (str): Path to the CSV file containing rental data.
        - current_rent (float): The user's current rent.
        """
        self.data_file_path = data_file_path
        self.current_rent = current_rent
        self.df = pd.read_csv(data_file_path)

    def get_summary_stats(self, zipcode, bedroom, query_date_prior, query_date):
        """
        Calculate and return summary statistics for rentals filtered by ZIP code, 
        number of bedrooms, and query date range.
        
        Args:
        - zipcode (str): The ZIP code to filter the rental data.
        - bedroom (int): The number of bedrooms to filter the rental data.
        - query_date_prior (str): The start date for the query in 'YYYY-MM-DD' format.
        - query_date (str): The end date for the query in 'YYYY-MM-DD' format.
        
        Returns:
        - pd.DataFrame: A DataFrame containing the summary statistics.
        """
        # Filter the data based on the criteria
        sample_df = self.df[
            (self.df['Query_Zip_Code'].astype(str) == zipcode) &
            (self.df['Bedroom'] == bedroom) &
            (self.df['Query_Date'] >= query_date_prior) &
            (self.df['Query_Date'] <= query_date)
        ]

        # Calculate the descriptive statistics
        summary_stats = sample_df['Price'].describe().to_frame().T  # Transpose to make it one row
        summary_stats.columns = ['# Obs', 'Average', 'Standard Deviation', 
                                 'Min', '25th Percentile', 'Median', 
                                 '75th Percentile', 'Max']
        
        return summary_stats

    def summarize_current_rent(self):
        """
        Generates a summary comparing the user's current rent to the rental market statistics.
        Assumes that get_summary_stats was called prior to this method and the
        resulting DataFrame is passed here.

        Returns:
        - str: A summary statement.
        """
        # Check if 'self.summary_stats' has been set by a previous call to 'get_summary_stats'
        if not hasattr(self, 'summary_stats'):
            raise AttributeError('You must run get_summary_stats() before summarize_current_rent().')

        df = self.summary_stats
        current_rent = self.current_rent
        
        avg_rent = df['Average'].iloc[0]
        median_rent = df['Median'].iloc[0]
        percentile_25 = df['25th Percentile'].iloc[0]
        percentile_75 = df['75th Percentile'].iloc[0]
        
        comparison_to_avg = "above" if current_rent > avg_rent else "below"
        comparison_to_median = "above" if current_rent > median_rent else "below"

        summary = f"The estimated rent of \${current_rent:,.0f} is {comparison_to_avg} the average rent of {avg_rent:,.0f} "
        summary += f"and {comparison_to_median} the median rent of \${median_rent:,.0f}. "


        if current_rent <= percentile_25:
            summary += "This places the estimated rent in the lower 25% of the market. "
        elif current_rent <= median_rent:
            summary += "This places the estimated rent in the lower 50% of the market. "
        elif current_rent <= percentile_75:
            summary += "This places the estimated rent in the upper 50% of the market. "
        else:
            summary += "This places the estimated rent in the upper 25% of the market. "
        
        # Display the summary in Streamlit (assuming this is a Streamlit app)
        st.write(summary)

    def display_summary_stats(self, zipcode, bedroom, query_date_prior, query_date):
        """
        Fetches the summary statistics, displays them, and shows the rent comparison summary.
        """
        # Get the rental statistics DataFrame and store it as an instance variable
        self.summary_stats = self.get_summary_stats(zipcode, bedroom, query_date_prior, query_date)
        # ... (Display logic for stats, could be factored into another method)
        self.summarize_current_rent()  # Now uses the instance variable 'self.current_rent'
