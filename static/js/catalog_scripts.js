'use strict'

window.onload = function () {
    $('.catalog-ajax-wrapper').on('click', '.catalog-ajax-url', function (event) {
        event.preventDefault();
        if (event.target.hasAttribute('href')) {
            let link = event.target.href + 'ajax/';
            let link_array = link.split('/');
            console.log(link_array[3], link_array)
            if (link_array[3] === 'category') {
                $.ajax({
                    url: link,
                    success: function (data) {
                        $('.catalog-ajax-include').html(data.result);
                    },
                });

                event.preventDefault();
            }
        }
    });
}
