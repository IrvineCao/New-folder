def _get_query_from_file(file_path):
    # Helper function để đọc tệp
    from pathlib import Path
    # Xây dựng đường dẫn an toàn
    path = Path(__file__).parent / "sql" / file_path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Xử lý nếu không tìm thấy tệp
        return "" 

query_params = {
    "count": _get_query_from_file("kw_pfm_count.sql"),
    "data": _get_query_from_file("kw_pfm_data.sql"),
}

def get_query(query_name):
    """
    Get a query by name from the pre-loaded dictionary.
    """
    return query_params.get(query_name, "")