import os
from flask import Flask,render_template,request, Blueprint, flash, redirect
import pickle
import numpy as np

books_bp = Blueprint('books_bp', __name__, template_folder="templates")

# Get the absolute path to the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths to the pickle files in the 'static' folder
popular_pkl_path = os.path.join(script_dir, 'static', 'popular.pkl')
pt_pkl_path = os.path.join(script_dir, 'static', 'pt.pkl')
books_pkl_path = os.path.join(script_dir, 'static', 'books.pkl')
similarity_scores_pkl_path = os.path.join(script_dir, 'static', 'similarity_scores.pkl')

# Load your recommendation system data using the absolute file paths
popular_df = pickle.load(open(popular_pkl_path, 'rb'))
pt = pickle.load(open(pt_pkl_path, 'rb'))
books = pickle.load(open(books_pkl_path, 'rb'))
similarity_scores = pickle.load(open(similarity_scores_pkl_path, 'rb'))

# app=Flask(__name__)
# app.secret_key = 'my_secret_key_here'

# @books.route('/books')

@books_bp.route('/')
def index():
    return render_template('books.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),

    )

@books_bp.route('/recommend')
def recommend_ui():
    return render_template('books_recommend.html')

@books_bp.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    
    # Check if the user input exists in the index
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:
        flash("Book not found. Please check the spelling and try again.", "error")
        return redirect('/books/recommend')
    
    # Perform recommendation logic
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    
    if not data:
        flash("No recommendations available for this book.", "info")
    
    return render_template('books_recommend.html', data=data)

    
# if __name__=='__main__':
#     app.run(debug=True)