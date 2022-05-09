from statistics import mean
from catalogue.models import Ratings
from user_profile.models import UserProfile


def calc_rating(request):
    ratings = Ratings.objects.filter(user_id=request.user.id)
    rating_score = 0
    if len(ratings) > 0:
        rating_score = mean([x.rating for x in ratings])
    return {'ratings': ratings, 'rating': str(round(rating_score))}


def get_profile(request):
    user_profile = UserProfile.objects.filter(user_id=request.user.id)
    return {'user_profile': user_profile}
