/**
 * Created by irish on 16/9/17.
 */
$(function () {
   $.ajax({
        url: '/cart',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.code === 0) {
                result.data.forEach(function(product) {
                    $('.products').append('<a class="product" href="product.html?pid='+product.id+'"><p class="description">'+product.product_name+'</p><span class="price">价格：'+product.product_price+'</span></a>');
                });
            } else {
                alert(result.msg);
            }
        }
    });
});