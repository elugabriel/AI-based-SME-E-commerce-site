from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_cart_recommendations(cart_items):
    all_products = Product.query.all()

    # Ensure all product attributes are strings to avoid NoneType issues
    product_texts = [
        (p.name or "") + " " + (p.category or "") + " " + (p.description or "")
        for p in all_products
    ]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(product_texts)

    # Extract product IDs from the cart items
    purchased_product_ids = [p["id"] for p in cart_items]

    # Find the indices of purchased products in all_products
    purchased_indices = [i for i, p in enumerate(all_products) if p.id in purchased_product_ids]

    if not purchased_indices:
        return []  # No recommendations if no valid products in the cart

    # Compute the user profile as the average TF-IDF vector of purchased items
    user_vector = tfidf_matrix[purchased_indices].mean(axis=0)

    # Compute similarity between the user's interest profile and all products
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Sort product indices by similarity score, excluding already purchased products
    recommended_indices = [
        i for i in similarity_scores.argsort()[::-1] if all_products[i].id not in purchased_product_ids
    ][:5]  # Select top 5 recommendations

    # Return the recommended products
    recommended_products = [all_products[i] for i in recommended_indices]

    return recommended_products
