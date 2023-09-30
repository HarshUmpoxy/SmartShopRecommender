GitHub link: https://github.com/HarshUmpoxy/SmartShopRecommender
Drive Demo link: https://drive.google.com/drive/folders/1ViHojlfmizjQ2nwZAS-K27mKLEfPhkjB?usp=sharing

# Smart Shop Recommender

Welcome to the Smart Shop Recommender project! This platform combines Fashion, Electronics, and Books Recommendation Systems along with an Admin section. It enhances the shopping experience by providing personalized recommendations across different product categories.

## Datasets

- [Fashion Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)
- [Books Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
- [Electronics Dataset](https://www.kaggle.com/datasets/vibivij/amazon-electronics-rating-datasetrecommendation/download?datasetVersionNumber=1)

## Algorithms and Working

### Fashion Recommendation System

The Fashion Recommendation System employs collaborative and content-based filtering algorithms. Collaborative filtering suggests items based on user interactions, while content-based filtering leverages product attributes for suggestions. Data preprocessing is critical and important for making correct pkl files. 

### Electronics Recommendation System

The Electronics Recommendation System utilizes rank, collaborative and content-based filtering methods. Collaborative filtering recommends products based on user preferences, and content-based filtering suggests items based on their attributes. Each user obj is assigned an integer for all users.

### Books Recommendation System

The Books Recommendation System employs collaborative and content-based filtering techniques. Collaborative filtering suggests books based on user interactions, while content-based filtering uses book attributes for suggestions.

## Features and Functionalities

- Secure User Registration and Login with Hashed Authentication
- Personalized Product Recommendations across Fashion, Electronics, and Books
- Admin Section with Secure Login, MySQL-Based Reports, and Insights
- Integration of an External API for Product Images
- User-Friendly UI for Seamless Interaction and Exploration

## Getting Started

1. Install dependencies from `requirements.txt`: `pip install -r requirements.txt`
2. Set-up and download the required dataset files in the specified locations (check the code txt's)
3. Run the app: `python app.py`

## Project Structure

- `app.py`: Main application entry point.
- `fashion_app.py`, `electronics_app.py`, `books_app.py`: Individual recommendation systems.
- `admin_app.py`: Admin functionalities and reports.
- `static/`: Static files (CSS, images, etc.).
- `templates/`: HTML templates for UI.

## Fork/Clone and Happy Develop!!!

