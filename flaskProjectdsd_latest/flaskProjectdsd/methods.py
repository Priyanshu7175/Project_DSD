from google.cloud import bigtable
from google.cloud.bigtable import row_filters
import pandas as pd
from utils import format_time

client = bigtable.Client(project='norse-acrobat-444522-a3', admin=True)
instance = client.instance('yelp-project')
table = instance.table('business')

def get_single_business_data(row_key):
    row_key = row_key
    row = table.read_row(row_key)

    row_data = {
        'business_id': row.row_key.decode()  # Store the row key (decode byte string to string)
    }

    for column_family_id, columns in row.cells.items():
        for column, cell_values in columns.items():
            for cell in cell_values:
                row_data[f"{column.decode()}"] = cell.value.decode()

    hours = eval(row_data['hours'])
    formatted_time = {}
    for day, time in hours.items():
        start_time, end_time = time.split('-')
        formatted_start = format_time(start_time)
        formatted_end = format_time(end_time)
        formatted_time[day] = f'{formatted_start}-{formatted_end}'

    categories = [category.strip() for category in row_data['categories'].split(",")]
    return {
        'business_id': row_data['business_id'],
        'name': row_data['name'],
        'address': row_data['address'],
        'city': row_data['city'],
        'state': row_data['state'],
        'postal_code': row_data['postal_code'],
        'categories': categories,
        'review_count': row_data['review_count'],
        'stars': row_data['stars'],
        'hours': formatted_time
    }

def get_all_business_data():
    rows = table.read_rows(limit=200000)

    data = []

    # Iterate over each row
    for row in rows:
        row_data = {
            'business_id': row.row_key.decode()
        }

        for column_family_id, columns in row.cells.items():
            for column, cell_values in columns.items():
                for cell in cell_values:
                    row_data[f"{column.decode()}"] = cell.value.decode()

        data.append(row_data)
    df = pd.DataFrame(data)

    return df

def get_business_reviews(business_id):
    reviews_table = instance.table('reviews')
    rows = reviews_table.read_rows(limit=200000)

    data = []
    for row in rows:
        row_data = {
            'review_id': row.row_key.decode()
        }

        for column_family_id, columns in row.cells.items():
            for column, cell_values in columns.items():
                row_data[f"{column.decode()}"] = cell_values[0].value.decode()

        data.append(row_data)

    df = pd.DataFrame(data)

    df = df[df['business_id'] == business_id]

    return df

