import streamlit as st
import pandas as pd
import datetime as dt
import pandas as pd

from src.PropertyFinder import PropertyFinder
from src.GaugeChart import GaugeChart
from src.RentalListingMap import RentalListingMap
from src.RentalSummaryStats import RentalSummaryStats
from src.NearbyRentalListings import NearbyRentalListings
from src.RentalAnalytics import RentalAnalytics
from src.CraigslistRentalListingsScraper import CraigslistRentalListingsScraper

st.set_option('deprecation.showPyplotGlobalUse', False)

# Constants
DATA_FILE_PATH = "Data/CraigsList_Rental_Listings.csv"
MAPBOX_TOKEN = "YOUR_MAPBOX_TOKEN"  

def user_input_sidebar():
    with st.sidebar.form(key='input_form'):
        property_address = st.text_input("Enter Zipcode", value="94608")
        bedroom = st.slider("Number of Bedrooms", min_value=0,  max_value=5, value=2)
        total_listings = st.slider("Number of Rental Listings", min_value=1, max_value=10, value=5)

        estimated_rent = st.number_input("Estimated Rent", min_value=0, value=2500, step=100)

        # Derive additional required variables
        miles = 1
        zipcode = property_address[-5:]
        query_date = dt.datetime.now().strftime("%Y-%m-%d")
        query_date_prior = (dt.datetime.now() - dt.timedelta(days=7)).strftime("%Y-%m-%d")

        # Submit button for the form
        submit_button = st.form_submit_button(label='Submit')

    return {
        'property_address': property_address,
        'zipcode': zipcode,
        'miles': miles,
        'total_listings':total_listings,
        'bedroom': bedroom,
        'estimated_rent': estimated_rent,
        'query_date': query_date,
        'query_date_prior': query_date_prior,
        'submit_button': submit_button
    }


def main():
    # Sidebar
    st.sidebar.title("Rental Search Criteria")
    property_details = user_input_sidebar()

    if property_details['submit_button']:
        with st.spinner("Downloading Rental Listings ..."):
            scraper = CraigslistRentalListingsScraper(
                zipcode=property_details['zipcode'], 
                miles=1, 
                bedrooms = property_details['bedroom'],
                sample_size=property_details['total_listings']
                )
            listings = scraper.scrape_listings()
            if listings:
                scraper.save_to_csv(DATA_FILE_PATH)

            st.write(""" # Rental Property Finder """)
        
            #display_user_input(property_details)
            df_properties = pd.read_csv(DATA_FILE_PATH)

            # Display Summary Stats 
            display_rental_stats( property_details)

            # Top-level columns
            col1, col2 = st.columns(2)

            with col1:

                # Display High Level Overview of Local Market with Metrics
                display_gauge_chart(df_properties, property_details)

            with col2:
                # Display Nearby Properties Map
                display_rental_map(df_properties, property_details)

            st.write(""" # Current Rental Listings """)

            # Display listings that match user criteria
            display_nearby_rental_listings(property_details)

        #    # Top-level columns
        #     col3, col4 = st.columns(2)

        #     with col3:
            # Display plot price regression
            display_plot_price_with_regression(property_details)

            # with col4:
            # Display price boxplot 
            display_plot_price_by_bedroom_boxplot(property_details)


    else:
        st.write(""" # Are you paying too much in rent?""")


def display_user_input(details):
    st.write("The entered details are:")
    st.write(f"ZIP Code: {details['zipcode']}")
    st.write(f"Radius in Miles: {details['miles']}")
    st.write(f"Number of Bedrooms: {details['bedroom']}")
    st.write(f"Estimated Rent: ${details['estimated_rent']}")

def display_gauge_chart(df_properties, details):
    gauge_chart = GaugeChart(DATA_FILE_PATH)
    gauge_chart.get_chart(
        zipcode=details['zipcode'],
        bedroom=details['bedroom'],
        estimatedRent=details['estimated_rent'],
        queryDatePrior=details['query_date_prior'],
        queryDate=details['query_date']
    )


def display_rental_map(df_properties, details):
    property_finder = PropertyFinder(df_properties, details['property_address'])
    nearby_properties, target_lon, target_lat = property_finder.find_within_radius(details['miles'])
    nearby_properties_df = nearby_properties[[ 'Address','Longitude', 'Latitude']]

    rental_map = RentalListingMap(MAPBOX_TOKEN)
    rental_map.render_map(nearby_properties_df, target_lon=target_lon, target_lat=target_lat)


def display_rental_stats( details):

    # Initialize the class with the path to the data file
    rental_stats = RentalSummaryStats(DATA_FILE_PATH,  current_rent=details['estimated_rent'])
    # Display the summary stats table with the corresponding filters in Streamlit
    rental_stats.display_summary_stats(
                        zipcode=details['zipcode'],
                        bedroom=details['bedroom'],
                        query_date_prior=details['query_date_prior'],
                        query_date=details['query_date']
    )

def display_nearby_rental_listings(details):
    # Instantiate the class with the path to the data file and the user's current rent
    rental_listings = NearbyRentalListings(DATA_FILE_PATH, current_rent=details['estimated_rent'])

    # Get the nearby rental properties
    nearby_properties = rental_listings.get_nearby_properties(
            zipcode=details['zipcode'],
            bedroom=details['bedroom'],
            query_date_prior=details['query_date_prior'],
            query_date=details['query_date']
    )

    # Display the rental properties with clickable URLs, which requires using Streamlit to write the DataFrame as HTML
    clickable_properties = NearbyRentalListings.display_nearby_properties(nearby_properties)

    # In a Streamlit app, you would then write:
    st.write(clickable_properties.to_html(escape=False, index=False), unsafe_allow_html=True)


def display_plot_price_with_regression(details):

    rental_analytics = RentalAnalytics(DATA_FILE_PATH)
    # Plotting
    # st.title('Rental Price Analysis')

    st.subheader('Price vs. Square Footage')
    fig = rental_analytics.plot_price_with_regression(
                        zipcode=details['zipcode'],
                        bedroom=details['bedroom'],
                        query_date_prior=details['query_date_prior'],
                        query_date=details['query_date'])
    st.pyplot(fig)

def display_plot_price_by_bedroom_boxplot(details):
    rental_analytics = RentalAnalytics(DATA_FILE_PATH)
    # Plotting
    st.subheader('Price Boxplot')
    fig = rental_analytics.plot_price_by_bedroom_boxplot(
                    zipcode=details['zipcode'],
                    bedroom=details['bedroom'],
                    query_date_prior=details['query_date_prior'],
                    query_date=details['query_date'])
    st.pyplot(fig)


#     # Generate plots
#     st.plot(rental_analytics.plot_price_with_regression(df_filtered))
# rental_analytics.plot_price_by_bedroom_boxplot(df_filtered)



if __name__ == "__main__":
    main()
