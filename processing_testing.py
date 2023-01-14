# from UserModel import _____
# ONCE KEVIN MAKES IT A FUNCTION ADD AS IMPORT AND REMOVE recommend_product FUNCTION FROM THIS FILE
# from InputProcessor import process_input
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import time

#

def process_input(filename) -> list[list[str]]:
    file = open(filename, "r")
    file = file.read()
    file = file.lower()
    products = file.split("\n\n")
    product_list: list[list[str]] = [['id', 'asin', 'title', 'group', 'salesrank', 'similar', 'categories', 'total_reviews', 'avg_rating']]
    for product in products:
        if 'title' in product:
            lines = product.split('\n')
            id = lines[0].split()[-1]
            asin = lines[1].split()[-1]
            title = lines[2].split('title: ')[-1]
            group = lines[3].split()[-1]
            salesrank = lines[4].split()[-1]
            similar = lines[5].split()[1]
            category_count = int(lines[6].split()[-1])
            categories = set()
            for i in range(category_count):
                for category_raw in lines[7 + i].split('|'):
                    category = category_raw.split('[')[0]
                    if not category.isspace():
                        categories.add(category)
            total_reviews = lines[7 + category_count].split()[2]
            avg_rating = lines[7 + category_count].split()[7]
            product_list.append([id, asin, title, group, salesrank, similar, categories, total_reviews, avg_rating])
    return product_list

def dictionarize(file_read_output):
    list_of_dict = []
    file_read_output.pop(0)
    for item in file_read_output:
        dict = {}
        dict['id'] = item[1]
        dict['tags'] = list(item[6])
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
    start_time = time.time()

    file_output = process_input(r"C:\Users\lpasu00555\Desktop\Daisy_Hackathon\amazon-meta-short.txt")

    new_purchased_products = [{'id': '0000000000', 'tags': ['christianity', 'subjects', 'sermons', 'clergy', 'books', 'preaching', 'religion & spirituality']},
                             {'id': '1111111111', 'tags': ['christianity', 'subjects', 'sermons', 'clergy', 'books', 'preaching', 'religion & spirituality']}]

    new_tagged_products = dictionarize(file_output)

    recs = recommend_product(new_purchased_products, new_tagged_products)

    print(file_output)

    for item in file_output:
        if item[1] in recs:
            print("\nI recommend: ", item[2], "\nThis item has tags: ", item[6], "\n")


    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Execution time:", elapsed_time, "seconds")









