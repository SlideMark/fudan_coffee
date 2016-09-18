/**
 * Created by irish on 16/9/14.
 */
$(function () {
    function getUrlParam(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
        return results == null  ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '))
    }
    var loading = $('.loading'), products = $('.products');
    $.ajax({
        url: '/account/signin',
        type: 'get',
        dataType: 'json',
        data: {
            code: getUrlParam('code')
        },
        success: function (result) {
            if (result.code === 0) {
                $('footer').removeClass('hide');
            }
        }
    });
    $.ajax({
        url: '/products',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            loading.addClass('hide');
            if(result.code === 0) {
                result.data.forEach(function(product) {
                    products.append('<a class="product" href="product.html?pid='+product.id+'"><img src="'+product.icon+'"><p class="description">'+product.description+'</p><span class="price">价格：'+product.price/100.0+'元</span></a>');
                });
            } else {
                alert(result.msg);
            }
        }
    });
});