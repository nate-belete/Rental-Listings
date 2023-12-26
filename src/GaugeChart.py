import numpy as np
import pandas as pd
from streamlit_echarts import st_echarts

class GaugeChart:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.df = pd.read_csv(data_file_path)

    def get_chart(self, zipcode, bedroom, estimatedRent, queryDatePrior, queryDate):
        # focus on query zip code
        sample_df = self.df[self.df['Query_Zip_Code'].astype(str) == zipcode].copy()

        # get prior 7 days of data
        sample_df = sample_df[(sample_df['Query_Date'] >= queryDatePrior) & (sample_df['Query_Date'] <= queryDate)].copy()

        # get summary stats based on user bedroom input
        sample_df = sample_df[(sample_df['Bedroom'] == bedroom)].copy()

        # calculate price percentiles
        min_price = sample_df['Price'].min()
        max_price = sample_df['Price'].max()

        # Check for NaN values and set a default value if needed
        min_price = min_price if pd.notna(min_price) else 0.0
        max_price = max_price if pd.notna(max_price) else 1000.0  # Set an arbitrary default max value

        # Calculation of the percentiles
        percentile_25_value = np.percentile(sample_df['Price'], 25)
        percentile_50_value = np.percentile(sample_df['Price'], 50)
        percentile_75_value = np.percentile(sample_df['Price'], 75)

        # calc mean
        mean_value = np.mean(sample_df['Price'])

        # Setting up the colors on the gauge chart
        options = {
                "tooltip": {
                    "formatter": "{a} <br/>{b} : {c}%"
                },
                "series": [
                    {
                        "name": "Price Range",
                        "type": "gauge",
                        "min": int(min_price),
                        "max": int(max_price),
                        "splitNumber": 4,  # Adjust the split number to have fewer ticks if needed
                        "axisLine": {
                            "lineStyle": {
                                "width": 30,
                                "color": [
                                    [0.25, "#98FB98"],
                                    [0.50, "#FFD700"],
                                    [0.75, "#GFA500"],
                                    [1, "#F08080"]
                                ]
                            }
                        },
                        "axisTick": {
                            "show": True,
                            "splitNumber": 5  # Adjust the number of ticks between split lines
                        },
                        "axisLabel": {
                            "distance": 35,  # The distance between the label and the axis line
                        },
                        "splitLine": {
                            "length": 10,  # The length of the split line
                        },
                        "pointer": {
                            "width": 5  # Width of the gauge pointer
                        },
                        "detail": {
                            "formatter": "{value}",
                            "offsetCenter": [0, '70%'],  # Adjust to control position of 'Your Rent' label
                            "fontSize": 18  # Adjust font size for 'Your Rent' label
                        },
                        "data": [{
                            "value": float(estimatedRent),
                            "name": "Rent"
                        }],
                    }
                ]
            }
        # Render the gauge chart
        return st_echarts(options=options, height="400px")