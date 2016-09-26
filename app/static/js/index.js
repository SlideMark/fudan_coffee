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
                    products.append('<div class="product"><span class="product-name">'+product.name+'</span><span class="product-price">'+product.price/100.0+'元</span><span class="addcart" data-productid="'+product.id+'">加入购物车</span><span class="buy" data-productid="'+product.id+'">购买</span></div>');
                });
            } else {
                showTips(result.msg);
            }
        }
    });

    function showdialog(product_id) {
        $.dialog({
           type : 'confirm',
           titleText: '选择支付方式',
           buttonText: {
               ok: '使用优惠购买',
               cancel: '使用余额购买'
           },
           onClickOk : function(){
                buyProductWithCoupon(product_id)
           },
           onClickCancel : function(){
                buyProductWithBalance(product_id)
           },
           contentHtml : '<p>不能同时使用余额和优惠额度。</p><p>请选用余额或者优惠券中的一种方式进行支付, 不足部分将通过微信支付。</p>'
        });
     }
    products.on('click', '.buy', function () {
        var m = $(this);
        $.ajax({
            url: '/cart',
            type: 'post',
            dataType: 'json',
            data: {
                product_id: m.data('productid')
            },
            success: function (result) {
                if (result.code === 0) {
                    location.replace('/static/cart.html');
                } else {
                    showTips(result.msg);
                }
            }
        });
    });

    products.on('click', '.addcart', function () {
        var m = $(this);
        $.ajax({
            url: '/cart',
            type: 'post',
            dataType: 'json',
            data: {
                product_id: m.data('productid')
            },
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog('加入成功');
                } else {
                    showTips(result.msg);
                }
            }
        });
    });
});