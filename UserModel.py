from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# List of products that the user has previously purchased
purchased_products = [{'id': 1, 'tags': ['electronics', 'smartphone']},
                      {'id': 2, 'tags': ['books', 'novel']},
                      {'id': 3, 'tags': ['books', 'action', 'novel']}]

# Set of tagged products
tagged_products = [{'id': 4, 'tags': ['books', 'novel']},
                   {'id': 5, 'tags': ['books', 'action', 'novel']},
                   {'id': 6, 'tags': ['books', 'sci-fi', 'novel']},
                   {'id': 7, 'tags': ['books', 'thriller', 'novel']},
                   {'id': 8, 'tags': ['books', 'mystery', 'novel']}]

# Extract the tags of the products that the user has previously purchased
purchased_product_tags = [' '.join(product['tags']) for product in purchased_products]

# Extract the tags of all other products
other_product_tags = [' '.join(product['tags']) for product in tagged_products]


########## User Recommendation Logic ##########

# Create a dictionary for the tags in the tagged_products
all_tags = [tag for product in tagged_products for tag in product['tags']]
tag_counts = {}
for tag in all_tags:
    if tag in tag_counts:
        tag_counts[tag] += 1
    else:
        tag_counts[tag] = 1

# Create a set of the most common tags to ignore
ignore_tags = set(tag for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])

# Create a dictionary for the user's tags
user_tags = {}
for product in purchased_products:
    for tag in product['tags']:
        if tag in user_tags:
            user_tags[tag] += 1
        else:
            user_tags[tag] = 1

# Assign weights to the user's tags based on their frequency while ignoring the most common tags
tag_weights = {tag: count/sum(user_tags.values()) for tag, count in user_tags.items() if tag not in ignore_tags}


########## Product Recommendation Logic ##########

feature_vectors = []
for product in tagged_products:
    feature_vector = []
    for tag in product['tags']:
        if tag in tag_weights:
            feature_vector.append(tag_weights[tag])
        else:
            feature_vector.append(0)
    feature_vectors.append(feature_vector)

# Create a feature vector for the user's purchased products
user_feature_vector = [tag_weights.get(tag, 0) for tag in user_tags]


# Create a TfidfVectorizer to convert the tags into a TF-IDF representation
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(purchased_product_tags + other_product_tags)

# Create a nearest neighbors model
nn = NearestNeighbors(n_neighbors=3, metric='cosine')
nn.fit(tfidf)

# Find the 3 most similar products to the ones that the user has previously purchased
similar_product_indices = nn.kneighbors(user_feature_vector, return_distance=False)[0][:3]

# remove the products that the user has already purchased
similar_product_indices = [index for index in similar_product_indices if tagged_products[index]['id'] not in [product['id'] for product in purchased_products]]

# Extract the ids of the recommended products
recommended_product_ids = [tagged_products[index]['id'] for index in similar_product_indices]

# Output the ids of the recommended products
print("Recommended product IDs: ", recommended_product_ids)
