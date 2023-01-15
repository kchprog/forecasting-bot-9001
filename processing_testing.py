## Helper Functions

# from InputProcessor import process_input
# from Boilerplate_matrix__factorization import recommend_product


## Imports

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import time


## Data Converter

def dictionarize(file_read_output):
    list_of_dict = []
    file_read_output.pop(0)
    for item in file_read_output:
        dict = {}
        dict['id'] = item[1]
        dict['tags'] = list(item[6])
        dict['ratings'] = item[8]
        list_of_dict.append(dict)
    return list_of_dict


##

if __name__ == "__main__":
    start_time = time.time()

    file_output = process_input(r"C:\Users\lpasu00555\Desktop\Daisy_Hackathon\amazon-meta-short.txt")

    new_purchased_products = [{'id': '0000000000', 'tags': ['christianity', 'subjects', 'sermons', 'clergy', 'books', 'preaching', 'religion & spirituality'], 'ratings': '4.5'},
                             {'id': '1111111111', 'tags': ['christianity', 'subjects', 'sermons', 'clergy', 'books', 'preaching', 'religion & spirituality']}, 'ratings': '5']

    new_tagged_products = dictionarize(file_output)
    print(new_tagged_products)

    recs = recommend_product(new_purchased_products, new_tagged_products)

    print(file_output)

    for item in file_output:
        if item[1] in recs:
            print("\nI recommend: ", item[2], "\nThis item has tags: ", item[6], "\n")


    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Execution time:", elapsed_time, "seconds")









