class Product:
    def __init__(self, id, asin, title, group, similar, categories, avg_rating):
        self.id = id
        self.asin = asin
        self.title = title
        self.group = group
        self.similar = similar
        self.categories = categories
        self.avg_rating = avg_rating

    def display(self):
        print("Id: ", self.id)
        print("ASIN: ", self.asin)
        print("Title: ", self.title)
        print("Group: ", self.group)
        print("Similar products: ", self.similar)
        print("Categories: ", self.categories)
        print("Avg rating: ", self.avg_rating)
