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
    profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    if UserProfile.objects.filter(user_id=request.user.id).exists():
        user_profile = UserProfile.objects.filter(user_id=request.user.id)[0]
        if len(user_profile.profile_picture) > 0:
            profile_picture = user_profile.profile_picture
    else:
        user_profile = []

    return {'user_profile': user_profile,
            'user_profile_picture': profile_picture}
