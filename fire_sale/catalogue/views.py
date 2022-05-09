from django.shortcuts import render
from catalogue.models import Postings, Bids
from item.models import Items
from django.template.defaulttags import register
from django.http import JsonResponse


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


# open, date, itemid, name, item_pic, category, max_bid
# Create your views here.
def index(request):
    query = Postings.objects.all().order_by('-creation_date')
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(item__name__icontains=search_filter)
        post_item = get_post_item(search_query)
        return JsonResponse({'data': post_item})

    if 'sort_by' in request.GET:
        sort_filter = request.GET['sort_by']
        if sort_filter == 'name':
            sort_query = Postings.objects.all().order_by('item__name')
            post_item = get_post_item(sort_query)
        elif sort_filter == 'high_low':
            post_item = get_post_item_sort_price(True)
        elif sort_filter == 'low_high':
            post_item = get_post_item_sort_price(False)
        else:
            # Recent or all unexpected sort by filters
            sort_query = Postings.objects.all().order_by('-creation_date')
            post_item = get_post_item(sort_query)
        return JsonResponse({'data': post_item})

    context = {'data': get_post_item(query)}
    return render(request, 'catalogue/index.html', context)


def get_post_item(query):
    post_item = [{
        'name': x.item.name,
        'item_pic': x.item.item_picture,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'itemid': x.item_id
    } for x in query]
    return post_item


def get_post_item_sort_price(order):
    query = Postings.objects.all().order_by('-creation_date')
    post_items = get_post_item(query)
    sorted_post_items = sorted(post_items, key=lambda k: k['max_bid'], reverse=order)
    return sorted_post_items
