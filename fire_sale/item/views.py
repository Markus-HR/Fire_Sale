from datetime import datetime
from statistics import mean

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from static.python.EmailManager import sendmail

from item.forms.bid_form import BidCreateForm
from item.forms.posting_form import ItemCreateForm
from item.models import Items
from catalogue.models import Bids, Ratings
from catalogue.models import Postings


# Create your views here.
def index(request, id):
    post_id = get_post_id(id)
    post = get_object_or_404(Postings, pk=post_id)
    if not post.open:
        return redirect('catalogue-index')
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
    item = get_object_or_404(Items, pk=id)
    return render(request, 'item/index.html', {
        'form': form,
        'item': item,
        'images': get_images_lis(item),
        'date': post.creation_date,
        'seller': {'user': post.user.username, 'user_id': post.user_id},
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


def get_poster_name(post_id):
    pass


def get_images_lis(item):
    image_lis = [item.image1]
    if item.image2:
        image_lis.append(item.image2)
    if item.image3:
        image_lis.append(item.image3)
    if item.image4:
        image_lis.append(item.image4)
    if item.image5:
        image_lis.append(item.image5)
    return image_lis


def get_post_item(item_id, post_id):
    item = get_object_or_404(Items, pk=item_id)
    related_posts = get_related_posts(item.category_id, post_id)
    post_item = [{
        'name': x.item.name,
        'item_pic': x.item.image1,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'itemid': x.item_id,
        'has_accepted_bid': check_accepted_bid(x.id)[0],
    } for x in related_posts]
    return post_item


def check_accepted_bid(post_id):
    bids = Bids.objects.filter(posting_id=post_id, accept=True)
    if bids:
        return [True, [x.price for x in bids]]
    else:
        return [False, [0]]


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


# View Offers Section


def view_offers(request, id):
    post_id = get_post_id(id)
    return render(request, 'item/view_offers/offers.html', {
        'item': get_object_or_404(Items, pk=id),
        'seller_id': get_user_from_post_id(post_id),
        'bids': get_post_bids(post_id),
    })


def get_user_from_post_id(post_id):
    post = Postings.objects.filter(pk=post_id)[0]
    user = post.user_id
    return user


def accept_offer(request, bidid):
    instance = get_object_or_404(Bids, pk=bidid)
    Bids.objects.filter(pk=instance.pk).update(accept=True)
    send_accepted_email_notification(instance)
    send_declined_email_notifications(instance)
    return redirect('catalogue-postings')


def send_accepted_email_notification(bid_instance):
    name = bid_instance.user.username
    item = bid_instance.posting.item.name
    email = bid_instance.user.email
    subject = "Your Bid Was Accepted"
    message = f"""Hello {name},
An offer you made on {item} has been accepted!!
Please check out your accepted bids to proceed to checkout.
Thank you for using FireSale!

With the bestest of regards and loads of love, The FireSale Team"""
    sendmail(email, subject, message)


def send_declined_email_notifications(bid_instance):
    post = bid_instance.posting
    email_list = [x.user.email for x in Bids.objects.filter(posting_id=post.id)]
    email = ', '.join(map(str, email_list))
    item = bid_instance.posting.item.name
    subject = "Your Bid Was Declined"
    message = f"""Hello,
We regret to inform you that an offer you made on {item} has been declined!
Feel free to check out our market for other interesting items to buy!
Thank you for using FireSale!

With the bestest of regards and loads of love, The FireSale Team"""
    sendmail(email, subject, message)


def get_post_bids(post_id):
    post_bids = [{
        'p_bid_id': x.id,
        'price': x.price,
        'accepted': x.accept,
        'user': x.user.username,
        'user_id': x.user_id,
        'user_rating': calculate_user_rating(x.user_id),
    } for x in Bids.objects.filter(posting_id=post_id).order_by('-price')]
    return post_bids


def calculate_user_rating(u_id):
    ratings = Ratings.objects.filter(user_id=u_id)
    rating_score = 0
    if len(ratings) > 0:
        rating_score = mean([x.rating for x in ratings])
    return str(round(rating_score))
