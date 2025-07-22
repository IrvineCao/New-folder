from utils.config import PROJECT_ROOT
import streamlit as st

def _get_query_from_file(file_path: str) -> str:
    """Helper function to read SQL file safely."""
    path = PROJECT_ROOT / "data_logic" / "sql" / file_path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError as e:
        st.error(f"Query file not found: {path.resolve()}")
        raise e

query_params = {
    "data": _get_query_from_file("competition_landscape_data.sql"),
    "count": _get_query_from_file("competition_landscape_count.sql")
}

def get_query(query_name: str) -> str:
    """Gets a query by name from the pre-loaded dictionary."""
    return query_params.get(query_name, "")