# Rental Property Finder

This Streamlit application helps users to find, analyze, and compare rental property listings. The data is scraped from Craigslist and analyzed to present users with insightful metrics and visualizations.

## Features

- Scrape Craigslist rental listings based on a user's search criteria.
- Display statistical summaries of the local rental market.
- Visualize rental listings on an interactive map.
- Compare rental prices with estimated rent through gauge charts.
- Show regressions and boxplots to understand rental price trends.

## Setup

Before running the app, make sure you have installed all the necessary libraries listed in `requirements.txt`.

### Libraries Installation

```bash
pip install -r requirements.txt
```

### Important Note

You need to obtain a Mapbox token to use the mapping features. Once you have the token, replace "YOUR_MAPBOX_TOKEN" in the script with your actual token.

### Running the App

To run the app locally, navigate to the app's directory and run:
```bash
streamlit run app.py
```

## How to Use

To get started with the Rental Property Finder, follow these steps:

1. Enter your search criteria in the sidebar:
   - **Zipcode**: Input the target area's zipcode.
   - **Number of Bedrooms**: Select the desired number of bedrooms.
   - **Number of Rental Listings**: Choose how many listings you wish to view.
   - **Estimated Rent**: Enter your estimated budget for rent.
   
2. Click the `Submit` button to initiate the search and analysis.

Once submitted, explore a variety of visualizations and statistics:

- **Gauge Chart**: Compares your estimated rent against current listings to see if you are paying too much.
- **Rental Listing Map**: An interactive map that shows the location of nearby listings, helping you visualize where available properties are located.
- **Summary Stats**: Provides a high-level overview of the rental market in your area, with key metrics to inform your search.
- **Nearby Rental Listings**: Displays a list of rental properties that match your search criteria, making it easier to find suitable listings.
- **Price vs. Square Footage**: Analyzes the relationship between rental prices and property sizes, giving you an insight into value-for-money.
- **Price Boxplot by Bedroom**: Shows the distribution of rental prices based on the number of bedrooms, helping you understand market trends and set realistic expectations.

## Get Involved

Interested in contributing? Start by forking the repo, then submit your pull requests. For issues or suggestions, please use the issues page on the repository.

## License Information

Distributed under the MIT License. See `LICENSE` for more information.

## Shout Outs

Thanks to Streamlit for their amazing framework that powers interactive data applications and to Craiglist for their data.

## Questions? Suggestions?

Feel free to email us at [natebelete@gmail.com](mailto:natebelete@gmail.com) for any inquiries or feedback.