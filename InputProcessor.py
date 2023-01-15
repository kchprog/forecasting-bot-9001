## Raw Data Processing

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


file_output = process_input(r"C:\Users\lpasu00555\Desktop\Daisy_Hackathon\amazon-meta-short.txt")
print(file_output)
