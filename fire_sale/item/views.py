from django.shortcuts import render, get_object_or_404, redirect

from item.forms.bid_form import BidCreateForm
from item.models import Items
from catalogue.models import Bids
from catalogue.models import Postings
from user_profile.models import UserProfile


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
    return render(request, 'item/index.html', {
        'form': form,
        'item': get_object_or_404(Items, pk=id),
        'bids': get_bid_dict(post_id),
        'user_bid': get_user_max_bid(request.user.username, get_bid_dict(post_id))
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


def get_user_max_bid(user_name, bids_dict):
    if user_name in bids_dict:
        return max(bids_dict[user_name])
    else:
        return 0


def get_post_id(id):
    post_set = Postings.objects.all()
    for post in post_set.iterator():
        if post.item_id == id:
            return post.id


def get_user_name(id):
    user_set = UserProfile.objects.all()
    for user in user_set.iterator():
        if user.id == id:
            return user.user.username

