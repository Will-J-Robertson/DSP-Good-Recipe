from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix
import pandas as pd
from Customer.models import *
import numpy as np

# This function uses collaborative filtering to recommend recipes to the user
def collaborative_filtering(request):
    # The data from the tables 'recipe' and 'ratings' are converted to a panda dataframe
    recipe = pd.DataFrame(Recipe.objects.all().values())
    ratings = pd.DataFrame(Ratings.objects.all().values())

    # The data types for the id's and ratings are altered to fit the alogrithm
    ratings["recipeID_id"] = ratings["recipeID_id"].astype(str)
    ratings["userID_id"] = ratings["userID_id"].astype(str)
    ratings["rating"] = pd.to_numeric(ratings["rating"])

    # user and recipe indexes are created by matching the id's with an integer for ease of calculation 
    ratings["user_index"] = ratings["userID_id"].astype("category").cat.codes
    ratings["recipe_index"] = ratings["recipeID_id"].astype("category").cat.codes

    # A matrix is made combining all the ratings to the user_index and to recipe_index
    ratings_matrix = coo_matrix((ratings["rating"], (ratings["user_index"], ratings["recipe_index"])))
    ratings_mat = ratings_matrix.tocsr()

    # Ks nearest neighbours makes user of the matrix to calculate and gather the
    # most similar users based on the user's recipe ratings.
    similarity = cosine_similarity(ratings_mat[0,:], ratings_mat).flatten()
    indices = np.argpartition(similarity, -4)[-4:]

    # Makes a copy of the ratings dataset with the 4 similar users
    similar_users = ratings[ratings["user_index"].isin(indices)].copy()
    # Ensures that the similar users does not contain the user them self
    similar_users = similar_users[similar_users["userID_id"]!=str(request.user.id)]

    # The count and mean are calculated based upon the rating of the recipe
    recipe_recs = similar_users.groupby("recipeID_id").rating.agg(['count', 'mean'])
    recipe["recipeID_id"] = recipe["id"].astype(str)
    # Merges the recommended id's with the recipe details the id belongs to
    recipe_recs = recipe_recs.merge(recipe, how="inner", on="recipeID_id")
    # The number of ratings are divided by the number of users. 
    # Where the score of the recipes are calcualted
    recipe_recs["adjusted_count"] = recipe_recs["count"] * (recipe_recs["count"] / 4)
    recipe_recs["score"] = recipe_recs["mean"] * recipe_recs["adjusted_count"]
    user_rates = ratings.loc[ratings['userID_id'] == str(request.user.id)]

    # All of the recipes that match from user_rates to the recipeID are gathered
    recipe_recs = recipe_recs[~recipe_recs["recipeID_id"].isin(user_rates["recipeID_id"])]
    recipe_recs = recipe_recs[~recipe_recs["recipeID_id"].isin(recipe["id"])]

    # The recommended recipes with a mean greater than a value of 4 are gathered
    recipe_recs = recipe_recs[recipe_recs["mean"] >=4]
    top_recs = recipe_recs.sort_values("mean", ascending=False)
    recomended = top_recs["recipeID_id"]

    # The top 10 recipes with a mean higher than 4 are returned.
    recom = recomended.head(10)
    rec = recom.values.tolist()
    return(rec)



# This function uses content-based filtering to recommend recipes to the user
def content_based_filtering(request):
    user = request.user
    # The data from the tables 'recipe', 'ratings' and 'tags' are converted 
    # to a panda dataframe for calculations
    recipe = pd.DataFrame(Recipe.objects.all().values())
    ratings = pd.DataFrame(Ratings.objects.all().values())
    tags = pd.DataFrame(Tags.objects.all().values())

    # The id's are removed so the features of 'Tags' are easier to extract
    tags = tags.drop(['id'], axis=1)
    ratings = ratings.drop(['id'], axis=1)
    
    # The recipes are paired with the ratings that the user gave them
    User_ratings = ratings[ratings['userID_id'] == user.id]
    User_ratings = pd.merge(recipe, User_ratings, how='right', left_on=['id'], right_on=['recipeID_id'])
    tags = pd.merge(User_ratings, tags, how='right', left_on=['id'], right_on=['recipeID_id'])
    # The dataframe is the stripped away of all the recipe details
    # Whats left in the dataframe are the columns 'ratings' against all of the tags
    tags = tags.drop(['recipeID_id_x', 'userID_id','id','recipeName','process','recipe_image','ingredients','numFavourited','calories','PrepTime','shortDescription'], axis=1)
    tags = tags.rename(columns={"recipeID_id_y": "recipeID_id"})
    tags=tags.dropna()
    User_ratings = User_ratings.drop(['recipeID_id','userID_id','process','recipe_image','ingredients','numFavourited','calories','PrepTime','shortDescription'], axis=1)

    # The user ratings are placed into a matrix against the tags of every recipe
    User_ratings = pd.DataFrame(User_ratings.rating)
    User_profile = np.concatenate([User_ratings, tags], axis=1)

    # The tags and recipes are merged together.
    recipes = pd.merge(recipe, tags, how='right', left_on=['id'], right_on=['recipeID_id'])
    # The index is then set to the recipeID.
    recipes = recipes.set_index(recipes.recipeID_id)
    # Deleting the unnecessary columns.
    recipes.drop(['recipeName','shortDescription','PrepTime','calories','numFavourited','ingredients','recipe_image','process'], axis=1, inplace=True)

    # The features are then multiplied by the weights and the weighted average is taken.
    recommendation_table_df = (recipes.T.dot(User_profile)) / User_profile.sum()
    recommendation_table_df = recommendation_table_df.T
    # The recommendations are then sorted by the tag's 'rating'
    recommendation_table_df.sort_values(ascending=False, inplace=True, by=['rating'])

    # The recommended recipe ids are appended into an array from the ordered dataframe
    top_10_index = recommendation_table_df.index[:10].tolist()

    # All the recipes are gathered that match the recipe id in the array 'top_10_index'
    recommended_recipes = recipe.loc[recipe.index.isin(top_10_index)]
    recomended = recommended_recipes["id"]

    # The top 10 recipes are taken from the dataframe and
    # returned to be displayed on the front-end
    recom = recomended.head(10)
    rec = recom.values.tolist()
    return(rec)
