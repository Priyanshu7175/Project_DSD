import os
import random
from flask import Flask, render_template, request
from methods import get_all_business_data, get_single_business_data, get_business_reviews
from model import get_restaurants_recommendation

app = Flask(__name__)

# Helper function to fetch random image filenames from the 'static/images' folder
def get_random_image():
    image_folder = os.path.join(app.root_path, 'static/images')
    available_images = [
        f for f in os.listdir(image_folder) 
        if os.path.isfile(os.path.join(image_folder, f))
    ]
    return random.choice(available_images) if available_images else "not_available.jpg"

@app.route('/')
def index():  
    return render_template('index.html')

@app.route('/recommendation', methods=['GET'])
def search():
    search_input = request.args.get('search').strip()

    data = get_all_business_data()

    # Check if the restaurant exists
    restaurant_exists = data[data['name'] == search_input].empty is False
    if not restaurant_exists:
        random_image = get_random_image()
        return render_template(
            'recommendation.html', 
            restaurant_exists=restaurant_exists, 
            restaurant_name=search_input, 
            random_image=random_image
        )

    restaurants = get_restaurants_recommendation(data, search_input)

    recommended_restaurants = []

    # Loop through DataFrame rows as (index, Series) pairs
    for _, row in restaurants.iterrows():
        # Convert row to dictionary
        row_dict = row.to_dict()
        if row_dict['name'] != search_input:
            categories = [category.strip() for category in row_dict['categories'].split(",")]
            random_image = get_random_image()  # Assign a random image
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
                'image': random_image,  # Include the image in the context
            })

    return render_template(
        'recommendation.html', 
        restaurant_exists=restaurant_exists, 
        restaurant_name=search_input, 
        restaurants=recommended_restaurants
    )

@app.route('/recommendation/<business_id>')
def business_details(business_id):
    business_details = get_single_business_data(business_id)
    reviews = get_business_reviews(business_id)
    reviews = reviews.to_dict(orient='records')

    return render_template(
        'details.html', 
        business=business_details, 
        reviews=reviews
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080',debug=True)
