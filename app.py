

from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
from datetime import timedelta
from datetime import date


from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
print("Loaded DATABASE_URL:", DATABASE_URL)


# Load environment variables from the .env file
load_dotenv()
DATABASE_URL = os.getenv("postgresql://myuser:mypassword@localhost:5432/mydatabase")
ENV = os.getenv("ENV", "dev")


from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL loaded successfully.")


# UI: Date input
start_time = st.date_input("Start Date", value=date(2024, 1, 1))
end_time = st.date_input("End Date", value=date(2024, 12, 31))

@st.cache_data(show_spinner=False) # Optimized
def get_earliest_date():
    """
    Returns the earliest date from the 'start_time' column in the database.
    """
    engine = create_engine("postgresql+psycopg2://mars_user:max$studio89@llm-gateway-demo.postgres.database.azure.com:5432/studio_db")
    query = "SELECT MIN(start_time) AS earliest_date FROM public.llm_usage;"
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df["earliest_date"].iloc[0]

if st.button("Fetch Segments"):
    segments = get_unique_segments(start_time, end_time)
    st.success(f"Found {len(segments)} segments:")
    st.write(segments)

