import pandas as pd
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity

def get_restaurants_recommendation(data, search_input):
    data = data.drop_duplicates(subset='name')
    data = data.dropna()

    feature = data["categories"].tolist()
    tfidf = text.TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(feature)
    similarity = cosine_similarity(tfidf_matrix)

    indices = pd.Series(data.index, index=data['name'])

    index = indices[search_input]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[0:10]
    restaurantindices = [i[0] for i in similarity_scores]

    return data[['business_id', 'name', 'address', 'city', 'state', 'postal_code', 'categories', 'review_count', 'stars']].iloc[restaurantindices]