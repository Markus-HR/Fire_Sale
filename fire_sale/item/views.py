from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from item.forms.bid_form import BidCreateForm
from item.models import Items
from catalogue.models import Bids
from catalogue.models import Postings
from catalogue.models import Ratings
from user_profile.models import UserProfile
from statistics import mean



# Create your views here.
def index(request, id):
    post_id = get_post_id(id)
    #user = get_user()
    if request.method == 'POST':
        form = BidCreateForm(data=request.POST)
        if form.is_valid():
            bid = Bids()
            bid.user_id = request.user.id
            bid.posting_id = post_id
            bid.accept = False
            bid.price = request.POST["price"]
            bid.save()
            redirect('index/'+str(id))
    else:
        form = BidCreateForm()
    bids_lis = get_bids_lis(post_id)
    return render(request, 'item/index.html', {
        'form': form,
        'item': get_object_or_404(Items, pk=id),
        'bids': bids_lis,
        'max_bid': max(bids_lis),
        'user_bid': get_user_max_bid(request.user.id, bids_lis)
    })


def get_bid_dict(post_id):
    bids_dict = {}
    bid_set = Bids.objects.all()
    for bid in bid_set.iterator():
        if bid.posting_id == post_id:
            user_name = get_user_name(bid.user_id)
            if user_name in bids_dict:
                bids_dict[user_name].append(bid.price)
            else:
                bids_dict[user_name] = [bid.price]
    return bids_dict


def get_bids_lis(posting_id):
    bids_lis = []
    bid_set = Bids.objects.all()
    for bid in bid_set.iterator():
        if bid.posting_id == posting_id:
            bids_lis.append(bid)
    return sorted(bids_lis, reverse=True)


def get_user_max_bid(id, bids_lis):
    user_bids = []
    for bid in bids_lis:
        if bid.user_id == id:
            user_bids.append(bid.price)
    if user_bids:
        return max(user_bids)
    else:
        return 0


def get_post_id(id):
    post_set = Postings.objects.all()
    for post in post_set.iterator():
        if post.item_id == id:
            return post.id


def get_user_name(id):
    user_set = User.objects.all()
    for user in user_set.iterator():
        if user.id == id:
            return user.username


# View Offers Section

def view_offers(request, id):
    post_id = get_post_id(id)
    return render(request, 'item/view_offers/offers.html', {
        'item': get_object_or_404(Items, pk=id),
        'bids': get_post_bids(post_id),
    })


def accept_offer(request, bidid):
    instance = get_object_or_404(Bids, pk=bidid)
    Bids.objects.filter(pk=instance.pk).update(accept=True)
    return redirect('catalogue-postings')


def get_post_bids(post_id):
    post_bids = [{
        'p_bid_id': x.id,
        'price': x.price,
        'accepted': x.accept,
        'user': x.user.username,
        'user_rating': calculate_user_rating(x.user_id),
    } for x in Bids.objects.filter(posting_id=post_id).order_by('-price')]
    return post_bids


def calculate_user_rating(u_id):
    ratings = Ratings.objects.filter(user_id=u_id)
    rating_score = 0
    if len(ratings) > 0:
        rating_score = mean([x.rating for x in ratings])
    return str(round(rating_score))
