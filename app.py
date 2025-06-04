import streamlit as st
import psycopg2
import pandas as pd

# Replace these with your Supabase details
DB_CONFIG = {
    "host": "aws-0-ap-south-1.pooler.supabase.com",
    "port": 6543,
    "user": "postgres.rbjqxoloenpofdkctoph",
    "password": "866868",
    "database": "postgres"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_data(name, email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
            conn.commit()

def get_all_data():
    with get_connection() as conn:
        df = pd.read_sql("SELECT * FROM users;", conn)
    return df

# Streamlit UI
st.set_page_config(page_title="User Form", layout="centered")
st.title("📋 User Entry Form")

with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Insert")
    if submitted:
        if name and email:
            insert_data(name, email)
            st.success("Inserted successfully!")
        else:
            st.error("Both fields are required.")

st.markdown("### 📊 All Entries")
data = get_all_data()
st.dataframe(data, use_container_width=True)
