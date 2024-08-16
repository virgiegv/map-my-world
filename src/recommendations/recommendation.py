from sqlalchemy.orm import Session
from . import repository
from . import schemas

def get_recommendations(db: Session, goal : int):

    recommendations = set() #this set will contain the recommendations to return

    #we need to know what categories have never been reviewed
    #once we have that, for each of their location, we can recommend their (category, location) pair
    never_reviewed_categories = repository.get_categories_never_reviewed(db)
    for category in never_reviewed_categories:
        locations = category.locations
        for location in locations:
            recommendation = schemas.RecommendationWithIds(
                location=location.name,
                location_id=location.id,
                category=category.name,
                category_id=category.id,
                last_reviewed_date=None,
            )
            recommendations.add(recommendation)
            if len(recommendations) == goal:
                break
        if len(recommendations) == goal:
            break

    #if we have reached our goal of 10 recommendations, we return
    if len(recommendations) == goal:
        return list(recommendations)

    #now, there might be categories that have been recommended, but some of their locations haven't ever
    #for this, we're gonna query over locations, excluding the ones with the categories found before,
    #and get locations that have never been reviewed
    #then we can recommend their (category, location) pair
    never_reviewed_locations = repository.get_locations_without_categories(never_reviewed_categories)
    for location in never_reviewed_locations:
        recommendation = schemas.RecommendationWithIds(
            location=location.name,
            location_id=location.id,
            category=category.name,
            category_id=category.id,
            last_reviewed_date=None,
        )
        recommendations.add(recommendation)
        if len(recommendations) == goal:
            break

    # if we have reached our goal of 10 recommendations, we return
    if len(recommendations) == goal:
        return list(recommendations)

    #if we havent reached 10 recommendations yet, let's say we have n recommendations where n < 10
    #we can query over category_location_reviews and get the top n where last_reviewed_date is more than 30 days ago
    #ordered by how far the last_reviewed_date is, that means, ordered ascendently
    n = len(recommendations)
    reviews = repository.get_top_N_reviews_not_updated_in_a_month(db, n)

    #we transform the set of recommendations into a list so that we can append the rest of the recommendations while
    #keeping the order of last_reviewed_date so that the ones without a review date stay first
    recommendations = list(recommendations)
    for review in reviews:
        recommendation = schemas.RecommendationWithIds(
            location=review.review_location.name,
            location_id=review.location_id,
            category=review.review_category.name,
            category_id=review.category_id,
            last_reviewed_date=review.last_reviewed_date,
        )
        recommendations.append(recommendation)
        if len(recommendations) == goal:
            break

    return recommendations
