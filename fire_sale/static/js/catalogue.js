$(document).ready(function () {
    $('#search-btn').on('click', function (e) {
        e.preventDefault();
        var searchText = $('#search-box').val();
        $.ajax({
            url: '?search_filter=' + searchText,
            type: 'GET',
            success: function (resp) {
                var newHtml = resp.data.map(d => {
                    return `<div>
                                <a href="/item/${d.itemid}">
                                    <div class="card" style="width: 12rem;">
                                        <img src="${d.item_pic}" class="card-img-top" alt="...">
                                        <div class="card-body">
                                            <h6 class="card-title">${d.name}</h6>
                                            <p class="card-text">$ ${d.max_bid}</p>
                                        </div>
                                    </div>
                                </a>
                            </div>`
                });
                $('.cat-grid').html(newHtml.join(''));
                $('#search-box').val('');
            },
            error: function (xhr, status, error) {
                //TODO: Show Toaster / other error message
                console.error(error)
            }
        })
    })

    $('input[type=radio][name=cat-filter]').change(function(e) {
        e.preventDefault();
        var checked = $("input[name='cat-filter']:checked").val();
        var filter = 'recent'
        if (checked === '1') {
            filter = 'recent'
        } else if (checked === '2') {
            filter = 'name'
        } else if (checked === '3') {
            filter = 'high_low'
        } else if (checked === '4') {
            filter = 'low_high'
        }

        $.ajax({
            url: '?sort_by=' + filter,
            type: 'GET',
            success: function (resp) {
                var newHtml = resp.data.map(d => {
                    return `<div>
                                <a class="card-link" href="/item/${d.itemid}">
                                    <div class="card">
                                        <img src="${d.item_pic}" class="card-img-top" alt="...">
                                        <div class="card-body">
                                            <h6 class="card-title">${d.name}</h6>
                                            <p class="card-text">$ ${d.max_bid}</p>
                                        </div>
                                    </div>
                                </a>
                            </div>`
                });
                $('.cat-grid').html(newHtml.join(''));
            },
            error: function (xhr, status, error) {
                //TODO: Show Toaster / other error message
                console.error(error)
            }
        })
    })

    $('input[type=radio][name=cat-bid-filter]').change(function(e) {
        e.preventDefault();
        var checked = $("input[name='cat-bid-filter']:checked").val();
        var filter = 'all'
        if (checked === '1') {
            filter = 'every'
        } else if (checked === '2') {
            filter = 'accepted'
        }

        $.ajax({
            url: '?sort_by=' + filter,
            type: 'GET',
            success: function (resp) {
                var newHtml = resp.data.map(d => {
                    return `<div>
                                <a class="card-link" href="/item/${d.post.itemid}">
                                    <div class="card">
                                        <img src="${ d.post.item_pic }" class="card-img-top" alt="...">
                                        <div class="card-body">
                                            <h6 class="card-title">${d.name}</h6>
                                            <p class="card-text">$ ${d.post.user_min_bid} - $ ${d.post.user_max_bid}</p>
                                        </div>
                                    </div>
                                </a>
                            </div>`
                });
                $('.cat-grid').html(newHtml.join(''));
            },
            error: function (xhr, status, error) {
                //TODO: Show Toaster / other error message
                console.error(error)
            }
        })
    })

})