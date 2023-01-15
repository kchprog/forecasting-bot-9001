# def recommend_product(purchased_products, tagged_products):
#     # Extract the tags of the products that the user has previously purchased
#     purchased_product_tags = [' '.join(product['tags']) for product in purchased_products]
#
#     # Extract the tags of all other products
#     other_product_tags = [' '.join(product['tags']) for product in tagged_products]
#
#     # Create a TfidfVectorizer to convert the tags into a TF-IDF representation
#     vectorizer = TfidfVectorizer()
#     tfidf = vectorizer.fit_transform(purchased_product_tags + other_product_tags)
#
#     # Create a nearest neighbors model
#     nn = NearestNeighbors(n_neighbors=3)
#     nn.fit(tfidf)
#
#     # Find the 3 most similar products to the ones that the user has previously purchased
#     similar_product_indices = nn.kneighbors(vectorizer.transform(purchased_product_tags), return_distance=False)[0][:3]
#
#     # remove the products that the user has already purchased
#     similar_product_indices = [index for index in similar_product_indices if tagged_products[index]['id'] not in [product['id'] for product in purchased_products]]
#
#     # Extract the ids of the recommended products
#     recommended_product_ids = [tagged_products[index]['id'] for index in similar_product_indices]
#
#     return recommended_product_ids
#
# # # Recommend the most similar products
# # print("Recommended products: ", similar_products)