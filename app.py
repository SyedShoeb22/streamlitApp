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
