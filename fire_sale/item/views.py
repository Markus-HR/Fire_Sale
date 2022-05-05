from django.shortcuts import render, get_object_or_404

from item.forms.bid_form import BidCreateForm
from item.models import Items
from catalogue.models import Bids
from catalogue.models import Postings
from user_profile.models import UserProfile


# Create your views here.
def index(request, id):
    post_id = get_post_id(id)
    bids_dict = {}
    bids_lis = []
    bid_set = Bids.objects.all()
    for bid in bid_set.iterator():
        if bid.posting_id_id == post_id:
            user_name = get_user_name(bid.user_id_id)
            bids_dict[bid.price] = user_name
            bids_lis.append(bid)
    #user = get_user()
    user_bids = []
    for bid in bids_lis:
        if bid.user_id_id == 1:
            user_bids.append(bid.price)
    return render(request, 'item/index.html', {
        'item': get_object_or_404(Items, pk=id),
        'bids': bids_dict,
        'user_bid': max(user_bids),
    })


def create_bid(request):
    if request.method == 'POST':
        form = BidCreateForm(data=request.POST)
    else:
        form = BidCreateForm()
    return render(request, 'item/make_bid.html', {
        'form': form
    })


def get_post_id(id):
    post_set = Postings.objects.all()
    for post in post_set.iterator():
        if post.item_id_id == id:
            return post.id


def get_user_name(id):
    user_set = UserProfile.objects.all()
    for user in user_set.iterator():
        if user.id == id:
            return user.user.username

#def get_user(request):
#    current_user = request.user
#    return current_user.id
