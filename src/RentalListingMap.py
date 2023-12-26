import pandas as pd
import pydeck as pdk
import streamlit as st

class RentalListingMap:
    def __init__(self, mapbox_token):
        # Store the Mapbox access token upon class instantiation
        self.mapbox_token = mapbox_token
        #pdk.set_mapbox_access_token(self.mapbox_token)  # You can uncomment this if you prefer setting it here.

    def render_map(self, df, target_lon, target_lat):
        # Assuming `df` DataFrame contains columns 'Latitude', 'Longitude', and 'Description'
        target_data = {
            'Description': ['Target Location'],
            'Latitude': [target_lat],
            'Longitude': [target_lon],
            'color': [[0, 255, 0]]
        }
        target_df = pd.DataFrame(target_data)

        rental_layer = pdk.Layer(
            'ScatterplotLayer',
            data=df.drop_duplicates().head(20),
            get_position='[Longitude, Latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        )

        target_layer = pdk.Layer(
            'ScatterplotLayer',
            data=target_df,
            get_position='[Longitude, Latitude]',
            get_color='color',
            get_radius=200,
        )

        # Render the map with PyDeck
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=target_lat,
                longitude=target_lon,
                zoom=12,
                pitch=10,
            ),
            layers=[
                rental_layer,
                target_layer,
            ],
        ))
