'use strict'

window.onload = function () {
    let basketList = $('.basket-list')
    basketList.on('change', 'input[type=number].product-qty', function (event) {
        // console.log(event.target);x
        $.ajax({
            url: `/basket/change/${event.target.name}/quantity/${event.target.value}/`,
            success: function (data){
                console.log(data)
                basketList.html(data.basket_items);
                // $('.basket-summary')...
            },
        })
    })
}