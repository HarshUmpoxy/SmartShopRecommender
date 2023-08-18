import warnings
import numpy as np
import pandas as pd
import pickle
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

warnings.filterwarnings('ignore')

# Import the data set
df = pd.read_csv('C:/Users/HARSH KUMAR/Desktop/Electronics/archive/ratings_Electronics.csv', header=None)
df.columns = ['user_id', 'prod_id', 'rating', 'timestamp']
df = df.drop('timestamp', axis=1)

# Filtering users with 50 or more ratings
counts = df['user_id'].value_counts()
df_final = df[df['user_id'].isin(counts[counts >= 50].index)]

# Creating the interaction matrix of products and users based on ratings and replacing NaN value with 0
final_ratings_matrix = df_final.pivot(index='user_id', columns='prod_id', values='rating').fillna(0)

# Calculate the average rating for each product
average_rating = df_final.groupby('prod_id').mean()['rating']
count_rating = df_final.groupby('prod_id').count()['rating']
final_rating = pd.DataFrame({'avg_rating': average_rating, 'rating_count': count_rating})
final_rating = final_rating.sort_values(by='avg_rating', ascending=False)

# Adding user_index and setting it as the index
final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])
final_ratings_matrix.set_index(['user_index'], inplace=True)

# Save the data structures as Pickle files
with open('final_ratings_matrix.pkl', 'wb') as f:
    pickle.dump(final_ratings_matrix, f)

with open('final_rating.pkl', 'wb') as f:
    pickle.dump(final_rating, f)

print("Pickle files created successfully.")

# Creating the sparse matrix
final_ratings_sparse = csr_matrix(final_ratings_matrix.values)

# Singular Value Decomposition
U, s, Vt = svds(final_ratings_sparse, k=50)  # here k is the number of latent features

# Construct diagonal array in SVD
sigma = np.diag(s)

# Predicted ratings
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)
preds_df = pd.DataFrame(abs(all_user_predicted_ratings), columns=final_ratings_matrix.columns)
preds_matrix = csr_matrix(preds_df.values)

# Save the preds_matrix as a Pickle file
with open('preds_matrix.pkl', 'wb') as f:
    pickle.dump(preds_matrix, f)


# Perform Singular Value Decomposition (SVD)
num_latent_features = 50  # Change this value as needed
U, s, Vt = svds(final_ratings_sparse, k=num_latent_features)

# Save U, s, and Vt matrices as pickle files
with open('U.pkl', 'wb') as f:
    pickle.dump(U, f)

with open('s.pkl', 'wb') as f:
    pickle.dump(s, f)

with open('Vt.pkl', 'wb') as f:
    pickle.dump(Vt, f)

print("preds_matrix Pickle file created successfully.")
