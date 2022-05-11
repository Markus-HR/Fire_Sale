from datetime import datetime
from statistics import mean

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect


from item.forms.bid_form import BidCreateForm
from item.forms.posting_form import ItemCreateForm
from item.models import Items
from catalogue.models import Bids, Ratings
from catalogue.models import Postings


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
            redirect('item-index', id)
    else:
        form = BidCreateForm()
    bids_lis = get_bids_lis(post_id)
    return render(request, 'item/index.html', {
        'form': form,
        'item': get_object_or_404(Items, pk=id),
        'bids': bids_lis,
        'max_bid': get_max_bid(bids_lis),
        'user_bid': get_user_max_bid(request.user.id, bids_lis),
        'data': get_post_item(id, post_id)
    })


def create_posting(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ItemCreateForm(data=request.POST)
        if form.is_valid():
            item = form.save()
            item_post = Postings(item=item, open=True, creation_date=datetime.now(), user=request.user)
            item_post.save()
            return redirect('catalogue-index')
    else:
        form = ItemCreateForm()
    return render(request, 'item/create_posting.html', {
        'form': form
    })


def get_post_item(item_id, post_id):
    item = get_object_or_404(Items, pk=item_id)
    related_posts = get_related_posts(item.category_id, post_id)
    post_item = [{
        'name': x.item.name,
        'item_pic': x.item.item_picture,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'itemid': x.item_id
    } for x in related_posts]
    return post_item


def get_max_bid(bid_lis):
    if bid_lis:
        return max(bid_lis).price
    else:
        return 0


def get_related_posts(cat_id, post_id):
    related_lis = []
    post_set = Postings.objects.all()
    for post in post_set.iterator():
        if post.id == post_id:
            continue
        if post.item.category_id == cat_id:
            related_lis.append(post)
    return related_lis


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
    return render(request, 'item/view_offers/offers.html', {
        'item': get_object_or_404(Items, pk=id),
        'bids': get_post_bids(id),
    })


def accept_offer(request, bidid):
    instance = get_object_or_404(Bids, pk=bidid)
    Bids.objects.filter(pk=instance.pk).update(accept=True)
    return redirect('catalogue-index')


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
