import os
import streamlit as st
import psycopg2
import pandas as pd

# Use environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# (rest of your code unchanged)
def init_db():
    # Create table if it doesn't exist
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_entry(name, email, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message))
    conn.commit()
    cur.close()
    conn.close()

def get_all_entries():
    conn = get_connection()
    df = pd.read_sql("SELECT name, email, message FROM entries ORDER BY id DESC", conn)
    conn.close()
    return df

# ---------- Streamlit UI ----------

st.title("📋 Submit Your Info")

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Database init failed: {e}")

# Form for user input
with st.form("entry_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            insert_entry(name, email, message)
            st.success("✅ Entry submitted!")
        except Exception as e:
            st.error(f"❌ Failed to submit: {e}")

# Display table
st.markdown("---")
st.subheader("📄 Submitted Entries")
try:
    df = get_all_entries()
    st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching entries: {e}")
