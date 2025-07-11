def get_query_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

query_params = {
    "count": get_query_from_file('data_logic/sql/kwl_count.sql'),
    "data": get_query_from_file('data_logic/sql/kwl_data.sql')
}