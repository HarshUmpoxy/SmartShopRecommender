from flask import Flask, render_template, request, Blueprint
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds
import os

# app = Flask(__name__)
electronics_bp = Blueprint('electronics_bp', __name__, template_folder='templates', static_folder='static')

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the pickle file paths
final_rating_path = os.path.join(script_dir, 'final_rating.pkl')
preds_matrix_path = os.path.join(script_dir, 'preds_matrix.pkl')
final_ratings_matrix_path = os.path.join(script_dir, 'final_ratings_matrix.pkl')
U_path = os.path.join(script_dir, 'U.pkl')
s_path = os.path.join(script_dir, 's.pkl')
Vt_path = os.path.join(script_dir, 'Vt.pkl')

# Load the Pickle files
with open(final_rating_path, 'rb') as f:
    final_rating = pickle.load(f)

with open(preds_matrix_path, 'rb') as f:
    preds_matrix = pickle.load(f)

with open(final_ratings_matrix_path, 'rb') as f:
    final_ratings_matrix = pickle.load(f)

with open(U_path, 'rb') as f:
    U = pickle.load(f)

with open(s_path, 'rb') as f:
    s = pickle.load(f)

with open(Vt_path, 'rb') as f:
    Vt = pickle.load(f)

# Convert final_ratings_matrix to a sparse matrix
final_ratings_sparse = csr_matrix(final_ratings_matrix.values)

# Rank Based Recommendation Logic
def top_n_products(final_rating, n, min_interaction):
    print("top_n_products function called")
    recommendations = final_rating[final_rating['rating_count'] > min_interaction]
    recommendations = recommendations.sort_values('avg_rating', ascending=False)
    return recommendations.index[:n].tolist()

# Collaborative Based Recommendation Logic
def similar_users(user_index, interactions_matrix):
    similarity = []
    for user in range(0, interactions_matrix.shape[0]): #  .shape[0] gives number of rows
        
        #finding cosine similarity between the user_id and each user
        sim = cosine_similarity([interactions_matrix.loc[user_index]], [interactions_matrix.loc[user]])
        
        #Appending the user and the corresponding similarity score with user_id as a tuple
        similarity.append((user,sim))
        
    similarity.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [tup[0] for tup in similarity] #Extract the user from each tuple in the sorted list
    similarity_score = [tup[1] for tup in similarity] ##Extracting the similarity score from each tuple in the sorted list
   
    #Remove the original user and its similarity score and keep only other similar users 
    most_similar_users.remove(user_index)
    similarity_score.remove(similarity_score[0])
       
    return most_similar_users, similarity_score


# defining the recommendations function to get recommendations by using the similar users' preferences
def recommendations(user_index, num_of_products, interactions_matrix):
    
    #Saving similar users using the function similar_users defined above
    most_similar_users = similar_users(user_index, interactions_matrix)[0]
    
    #Finding product IDs with which the user_id has interacted
    prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[user_index] > 0)]))
    recommendations = []
    
    observed_interactions = prod_ids.copy()
    for similar_user in most_similar_users:
        if len(recommendations) < num_of_products:
            
            #Finding 'n' products which have been rated by similar users but not by the user_id
            similar_user_prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[similar_user] > 0)]))
            recommendations.extend(list(similar_user_prod_ids.difference(observed_interactions)))
            observed_interactions = observed_interactions.union(similar_user_prod_ids)
        else:
            break
    
    return recommendations[:num_of_products]


# Model-Based Collaborative Filtering Recommendation Logic
def recommend_items(user_index, interactions_matrix, preds_matrix, num_recommendations):
    # Get the user's ratings from the actual and predicted interaction matrices
    user_ratings = interactions_matrix[user_index, :].toarray().reshape(-1)
    user_predictions = preds_matrix[user_index, :].toarray().reshape(-1)

    # Creating a dataframe with actual and predicted ratings columns
    temp = pd.DataFrame({'user_ratings': user_ratings, 'user_predictions': user_predictions})
    temp['Recommended Products'] = np.arange(len(user_ratings))
    temp = temp.set_index('Recommended Products')

    # Filtering the dataframe where actual ratings are 0 which implies that the user has not interacted with that product
    temp = temp.loc[temp.user_ratings == 0]

    # Recommending products with top predicted ratings
    temp = temp.sort_values('user_predictions', ascending=False)  # Sort the dataframe by user_predictions in descending order

    # Get the recommended product indices
    recommended_indices = temp.index[:num_recommendations]

    return recommended_indices


@electronics_bp.route('/')
def home():
    return render_template('recommend_form.html')

@electronics_bp.route('/recommend_rank', methods=['GET', 'POST'])
def recommend_rank():
    if request.method == 'POST':
        num_recommendations = int(request.form['num_recommendations'])
        min_interaction = int(request.form['min_interaction'])
        print("num_recomm", num_recommendations)
        print("min_interaction required", min_interaction)
        recommended_products = top_n_products(final_rating, num_recommendations, min_interaction)
        print(recommended_products)
        return render_template('recommendations.html', recommendations=recommended_products)

    return render_template('recommend_form.html')

@electronics_bp.route('/recommend_collaborative', methods=['GET', 'POST'])
def recommend_collaborative():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        num_recommendations = int(request.form['num_recommendations'])

        recommended_products = recommendations(user_id, num_recommendations, final_ratings_matrix)

        return render_template('recommendations.html', recommendations=recommended_products)

    return render_template('recommend_form.html')


@electronics_bp.route('/recommend_model', methods=['GET', 'POST'])
def recommend_model():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        num_recommendations = int(request.form['num_recommendations'])
        print("user_id", user_id)
        print("num_recommendations", num_recommendations)

        recommended_products = recommend_items(user_id, final_ratings_sparse, preds_matrix, num_recommendations)
        print("recommended_products", recommended_products)

        return render_template('recommendations.html', recommendations=recommended_products)

    return render_template('recommend_form.html')


# if __name__ == '__main__':
#     app.run(debug=True)
