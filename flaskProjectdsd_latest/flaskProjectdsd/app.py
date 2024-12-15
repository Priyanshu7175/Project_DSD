from flask import Flask, render_template, request

from methods import get_all_business_data, get_single_business_data, get_business_reviews
from model import get_restaurants_recommendation

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/recommendation', methods=['GET'])
def search():
    search_input = request.args.get('search').strip()

    data = get_all_business_data()

    # check if restaurant exists
    restaurant_exists = data[data['name'] == search_input].empty is False
    if not restaurant_exists:
        return render_template('recommendation.html', restaurant_exists=restaurant_exists, restaurant_name=search_input)

    restaurants = get_restaurants_recommendation(data, search_input)

    recommended_restaurants = []

    # Loop through DataFrame rows as (index, Series) pairs
    for _, row in restaurants.iterrows():
        # convert row to dictionary
        row_dict = row.to_dict()
        if row_dict['name'] != search_input:
            categories = [category.strip() for category in row_dict['categories'].split(",")]
            recommended_restaurants.append({
                'business_id': row_dict['business_id'],
                'name': row_dict['name'],
                'address': row_dict['address'],
                'city': row_dict['city'],
                'state': row_dict['state'],
                'postal_code': row_dict['postal_code'],
                'categories': categories,
                'review_count': row_dict['review_count'],
                'stars': row_dict['stars'],
            })

    return render_template('recommendation.html', restaurant_exists=restaurant_exists, restaurant_name=search_input, restaurants=recommended_restaurants)

@app.route('/recommendation/<business_id>')
def business_details(business_id):

    business_details = get_single_business_data(business_id)
    reviews = get_business_reviews(business_id)
    reviews = reviews.to_dict(orient='records')

    return render_template('details.html', business = business_details, reviews = reviews)

if __name__ == '__main__':
    app.run(debug=True)
