import Product
import pandas as pd

# Open the input file

def process_input(filename):

    product_list = []

    file = open(filename, "r", encoding="latin1")
    file = file.read()
    file = file.lower()
    sentence_list = file.split("\n")

    pointer = 0
    while pointer < len(sentence_list):
        line = sentence_list[pointer].strip()# remove leading and trailing whitespaces

        # if the line is empty: start a new product
        if line == "" or len(line) < 2:
            id = None
            asin = None
            title = None
            group = None
            similar = None
            categories = None
            avg_rating = None

            pointer += 1
            while not (line == "" or len(line) < 2):
                line = sentence_list[pointer].strip()
                if line.split()[0] == "Id:":
                    id = line.split()[-1]
                elif line.split()[0] == "ASIN:":
                    asin = line.split()[-1]
                elif line.split()[0] == "title:":
                    title = line
                elif line.split()[0] == "group:":
                    group = line.split(": ")[-1]
                elif line.split()[0] == "similar:":
                    similar = line.split[2:-1]
                elif line.split()[0] == "categories:":
                    categories = {}

                    pointer += 1
                    line = sentence_list[pointer].strip()
                    
                    while line[0] == "|":
                        line_categories = line.split("|")
                        for category in line_categories:
                            if category != "":
                                categories.add(category)
                        pointer += 1
                        line = sentence_list[pointer].strip()

                if line.split[0]("reviews:"):
                    total_reviews = line.split(": ")[1].split()[0]
                    avg_rating = (int(total_reviews), float(line.split(": ")[-1]))
                
                pointer += 1

                product_list.append(Product(id, asin, title, group, similar, categories, avg_rating))


    