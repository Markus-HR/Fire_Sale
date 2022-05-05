from django.shortcuts import render, get_object_or_404
from item.models import Items
from catalogue.models import Bids
from catalogue.models import Postings


# Create your views here.
def index(request, id):
    post_set = Postings.objects.all()
    for post in post_set.iterator():
        if post.item_id_id == id:
            post_id = post.id
            break
    bids_lis = []
    bid_set = Bids.objects.all()
    for bid in bid_set.iterator():
        if bid.posting_id_id == post_id:
            bids_lis.append(bid)
    return render(request, 'item/index.html', {
        'item': get_object_or_404(Items, pk=id),
        'bids': bids_lis,
    })
