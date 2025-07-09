import streamlit as st
from datetime import date

@st.cache_data(show_spinner=False) # Optimized
def get_unique_segments(start_time, end_time):
    """
    Returns a list of distinct segments in the selected time frame.
    """
    engine = create_engine(DATABASE_URL)
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

@st.cache_data(show_spinner=False) # Optimized
def get_earliest_date():
    """
    Returns the earliest date from the 'start_time' column in the database.
    """
    engine = create_engine(DATABASE_URL)
    query = "SELECT MIN(start_time) AS earliest_date FROM public.llm_usage;"
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df["earliest_date"].iloc[0]

earliest_date = get_earliest_date()
primary_key = "userPrincipalName"
