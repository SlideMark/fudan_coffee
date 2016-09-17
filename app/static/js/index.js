/**
 * Created by irish on 16/9/14.
 */
$(function () {
    var loading = $('.loading'), products = $('.products');
    $.ajax({
        url: '/products',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            loading.addClass('hide');
            if(result.code === 0) {
                result.data.forEach(function(product) {
                    products.append('<a class="product" href="product.html?pid='+product.id+'"><img src="'+product.icon+'"><p class="description">'+product.description+'</p><span class="price">价格：'+product.price+'</span></a>');
                });
            } else {
                alert(result.msg);
            }
        }
    });
})