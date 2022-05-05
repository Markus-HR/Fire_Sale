from django.shortcuts import render
from catalogue.models import Postings, Bids
from item.models import Items
from django.template.defaulttags import register


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


# Create your views here.
def index(request):
    # context_list = get_post_item()
    # context_dict = dict()
    # for index, value in enumerate(context_list):
    #     context_dict[index] = value
    context = {'postings': get_post_item()}
    return render(request, 'catalogue/index.html', context)


def get_post_item():
    postings = Postings.objects.all()
    items = Items.objects.all()
    bids = Bids.objects.all()
    post_items = []
    for post in postings:
        postitem = {}
        postitem = {'open': post.open, 'date': post.creation_date.date()}
        for item in items:
            if item.id == post.item_id_id:
                postitem['name'] = item.name
                postitem['item_pic'] = item.item_picture
                postitem['category'] = item.category
                break
        bid_price_list = []
        for bid in bids:
            if bid.posting_id_id == post.id:
                bid_price_list.append(bid.price)
        if bid_price_list == []:
            postitem['max_bid'] = 0
        else:
            postitem['max_bid'] = max(bid_price_list)
        post_items.append(postitem)
    return post_items
