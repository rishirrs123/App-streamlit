import streamlit as st
from datetime import date

# Dummy function: replace this with your actual logic
def get_unique_segments(start_date, end_date):
    return [{"Segment": "A", "Start": start_date, "End": end_date}]

st.title("Segment Fetcher")

start_date = st.date_input("Start Date", date.today())
end_date = st.date_input("End Date", date.today())

if st.button("Fetch Segments"):
    segments = get_unique_segments(start_date, end_date)
    st.write("Segments found:")
    st.dataframe(segments)

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
