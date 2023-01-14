# from UserModel import _____
# ONCE KEVIN MAKES IT A FUNCTION ADD AS IMPORT AND REMOVE recommend_product FUNCTION FROM THIS FILE
from InputProcessor import process_input
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def dictionarize(file_read_output):
    list_of_dict = []
    file_read_output.pop(0)
    for i in file_read_output:
        dict = {}
        dict['id'] = i[1]
        dict['tags'] = list(i[6])
        list_of_dict.append(dict)
    return list_of_dict

def recommend_product(purchased_products, tagged_products):
    # Extract the tags of the products that the user has previously purchased
    purchased_product_tags = [' '.join(product['tags']) for product in purchased_products]

    # Extract the tags of all other products
    other_product_tags = [' '.join(product['tags']) for product in tagged_products]

    # Create a TfidfVectorizer to convert the tags into a TF-IDF representation
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(purchased_product_tags + other_product_tags)

    # Create a nearest neighbors model
    nn = NearestNeighbors(n_neighbors=3)
    nn.fit(tfidf)

    # Find the 3 most similar products to the ones that the user has previously purchased
    similar_product_indices = nn.kneighbors(vectorizer.transform(purchased_product_tags), return_distance=False)[0][:3]

    # remove the products that the user has already purchased
    similar_product_indices = [index for index in similar_product_indices if tagged_products[index]['id'] not in [product['id'] for product in purchased_products]]

    # Extract the ids of the recommended products
    recommended_product_ids = [tagged_products[index]['id'] for index in similar_product_indices]

    return recommended_product_ids

# # Recommend the most similar products
# print("Recommended products: ", similar_products)

################

if __name__ == "__main__":

    file_output = process_input(r"C:\Users\lpasu00555\Desktop\Daisy_Hackathon\amazon-meta-short.txt")

    new_purchased_products = [{'id': '0000000000', 'tags': ['subjects', 'cooking, food & wine', 'baking', 'bread']},
                             {'id': '1111111111', 'tags': ['subjects', 'cooking, food & wine', 'baking', 'bread']},
                             {'id': '2222222222', 'tags': ['subjects', 'cooking, food & wine', 'baking', 'bread']}]
    new_tagged_products = dictionarize(file_output)

    print(recommend_product(new_purchased_products, new_tagged_products))






