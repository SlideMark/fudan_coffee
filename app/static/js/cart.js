/**
 * Created by irish on 16/9/17.
 */
$(function () {
    var empty = $('.empty'), products = $('.products');
   $.ajax({
        url: '/cart',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                result.data.forEach(function(product) {
                    products.append('<a class="product" href="product.html?pid='+product.id+'"><p class="description">'+product.product_name+'</p><span class="price">价格：'+product.product_price+'</span></a>');
                });
            } else {
                products.addClass('hide');
                $('footer').addClass('hide');
            }
        }
    });
});