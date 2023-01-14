import pandas as pd
from sklearn.decomposition import TruncatedSVD
import math

# List of products that the user has previously purchased
purchased_products = [{'id': 1, 'tags': ['electronics', 'smartphone']},
                      {'id': 2, 'tags': ['books', 'novel']},
                      {'id': 3, 'tags': ['books', 'action', 'novel']},
                      {'id': 4, 'tags': ['books', 'action', 'novel']},
                      {'id': 5, 'tags': ['books', 'action', 'novel']}
                      ]

# Set of tagged products
tagged_products = [{'id': 4, 'tags': ['books', 'novel']},
                   {'id': 5, 'tags': ['books', 'action', 'novel']},
                   {'id': 6, 'tags': ['books', 'sci-fi', 'novel']},
                   {'id': 7, 'tags': ['books', 'thriller', 'novel']},
                   {'id': 8, 'tags': ['books', 'mystery', 'novel']},
                   {'id': 9, 'tags': ['books', 'action', 'novel']}
                   ]

# Create a set of all tags
all_tags = set([tag for product in tagged_products for tag in product['tags']])

# Create a dataframe with one-hot encoded tags for each product
df = pd.DataFrame(tagged_products)
df = df.join(pd.DataFrame(df.pop('tags').apply(pd.Series).stack().reset_index(level=1, drop=True).rename('tags')))
df = df.join(pd.get_dummies(df.pop('tags'), prefix='', prefix_sep=''))

# Create a dictionary for the tags in the purchased products
purchased_tags = {}
for product in purchased_products:
    for tag in product['tags']:
        if tag in purchased_tags:
            purchased_tags[tag] += 1
        else:
            purchased_tags[tag] = 1

# Create a dictionary for the tags in the non-purchased products
non_purchased_tags = {}
for product in tagged_products:
    if product['id'] not in [p['id'] for p in purchased_products]:
        for tag in product['tags']:
            if tag in non_purchased_tags:
                non_purchased_tags[tag] += 1
            else:
                non_purchased_tags[tag] = 1

# Create a set of the most common tags to ignore
common_tags = set(tag for tag, count in non_purchased_tags.items() if count >= 2)
ignore_tags = all_tags - common_tags

# Remove the columns of the ignored tags from the dataframe
df = df.drop(columns=ignore_tags)

# Create a matrix with the tag weights for each product
matrix = []
for product in tagged_products:
    product_weights = []
    for tag in all_tags:
        if tag in product['tags']:
            product_weights.append(purchased_tags.get(tag, 0))
        else:
            product_weights.append(0)
    matrix.append(product_weights)

# Create a matrix factorization model
svd = TruncatedSVD(n_components=2)
svd_matrix = svd.fit_transform(matrix)

# Create a Dataframe with the SVD matrix 
df_svd = pd.DataFrame(svd_matrix, columns=['x', 'y'])
df_svd['id'] = [product['id'] for product in tagged_products]

# Reset the index of the df_svd dataframe
df_svd = df_svd.reset_index(drop=True)

# Create a boolean mask that filters out the rows that contain all the ignored tags
mask = ~df.drop(columns=['id']).eq(0).all(axis=1)

# filter the dataframe using the mask
df = df[mask]


# get the user's purchases id
purchased_ids = [product['id'] for product in purchased_products]

# find similar products
similar_products = df_svd[~df_svd['id'].isin(purchased_ids)].sort_values(by=['x', 'y'], ascending=False).head(3)

# Extract the ids of the recommended products
recommended_product_ids = similar_products['id'].tolist()

# Output the ids of the recommended
print("Recommended product IDs: ", recommended_product_ids)