from django.shortcuts import render
from catalogue.models import Postings, Bids
from django.template.defaulttags import register
from django.http import JsonResponse


#TODO make closed posts not show

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
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})

    if 'sort_by' in request.GET:
        sort_filter = request.GET['sort_by']
        if sort_filter == 'name':
            sort_query = Postings.objects.all().order_by('item__name')
            post_item = get_post_item(sort_query, request)
        elif sort_filter == 'high_low':
            post_item = get_post_item_sort_price(True, request)
        elif sort_filter == 'low_high':
            post_item = get_post_item_sort_price(False, request)
        else:
            # Recent or unexpected sort by filters
            sort_query = Postings.objects.all().order_by('-creation_date')
            post_item = get_post_item(sort_query, request)
        return JsonResponse({'data': post_item})

    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/index.html', context)


def get_post_item(query, request):
    post_item = [{
        'name': x.item.name,
        'item_pic': x.item.item_picture,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'has_accepted_bid': check_accepted_bid(x.id),
        'itemid': x.item_id,
        # 'user_max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id, user_id=request.user.id)], default=0),
        # 'user_min_bid': min([y.price for y in Bids.objects.filter(posting_id=x.id, user_id=request.user.id)], default=0),
    } for x in query]
    return post_item


def check_accepted_bid(post_id):
    bids = Bids.objects.filter(posting_id=post_id, accept=True)
    if bids:
        return True
    else:
        return False


def get_post_item_sort_price(rev_order, request):
    query = Postings.objects.all().order_by('-creation_date')
    post_items = get_post_item(query, request)
    sorted_post_items = sorted(post_items, key=lambda k: k['max_bid'], reverse=rev_order)
    return sorted_post_items


# My bids section
def my_bids(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(bids__user=request.user.id, item__name__icontains=search_filter)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})

    if 'sort_by' in request.GET:
        sort_filter = request.GET['sort_by']
        if sort_filter == 'accepted':
            sort_query = Postings.objects.filter(bids__user=request.user.id, bids__accept=True)
            post_item = get_post_item(sort_query, request)
        elif sort_filter == 'every':
            sort_query = Postings.objects.filter(bids__user=request.user.id)
            post_item = get_post_item(sort_query, request)
        else:
            # all or unexpected sort by filters
            sort_query = Postings.objects.filter(bids__user=request.user.id)
            post_item = get_post_item(sort_query, request)
        return JsonResponse({'data': post_item})

    query = Postings.objects.filter(bids__user=request.user.id)
    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/bids/my_bids.html', context)


# My postings section
def my_postings(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(user=request.user.id, item__name__icontains=search_filter)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})

    query = Postings.objects.filter(user=request.user.id)
    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/posting/my_postings.html', context)


