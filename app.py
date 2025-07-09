

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


# Date inputs
start_time = st.date_input("Start Date", value=date(2024, 1, 1))
end_time = st.date_input("End Date", value=date(2024, 12, 31))

# Function to get data
@st.cache_data(show_spinner=False)
def get_unique_segments(start_time, end_time):
    engine = create_engine("postgresql://myuser:mypassword@your-host:5432/mydatabase")
    query = """
    SELECT DISTINCT INITCAP(LOWER(TRIM(user_id->>'segment'))) AS segment
    FROM public.llm_usage
    WHERE start_time BETWEEN %s AND %s
      AND TRIM(user_id->>'segment') IS NOT NULL
      AND TRIM(user_id->>'segment') <> ''
      AND LOWER(TRIM(user_id->>'segment')) NOT IN ('api user', 'unknown')
    ORDER BY segment;
    """
    segments = pd.read_sql(query, engine, params=(start_time, end_time))["segment"].dropna().tolist()
    engine.dispose()

    updated_segments = []
    for seg in segments:
        if "anicura" in seg.lower():
            updated_segments.append("Petcare")
        else:
            updated_segments.append(seg)
    return sorted(set(updated_segments))

# Button to trigger data fetch
if st.button("Fetch Segments"):
    try:
        segments = get_unique_segments(start_time, end_time)
        st.success(f"Found {len(segments)} segments")
        st.write(segments)
    except Exception as e:
        st.error(f"Error: {e}")
