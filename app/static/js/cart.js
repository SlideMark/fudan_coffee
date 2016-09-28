/**
 * Created by irish on 16/9/17.
 */
$(function () {
    var empty = $('.empty'), products = $('.products'), st = 0;
    $.ajax({
        url: '/cart',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                result.data.forEach(function(product) {
                    products.append('<div class="product"><a href="product.html?pid='+product.id+'"><img src="'+product.product_icon+'" /><div class="product_info"><p class="description">'+product.product_name+'</p><span class="price">价格：'+product.product_price/100+'元</span></div></a><div class="product_num"><span class="minus" data-cartid="'+product.id+'">-</span><input type="text" data-num="'+product.num+'" data-cartid="'+product.id+'" value="'+product.num+'" class="num" /><span data-cartid="'+product.id+'" class="plus">+</span></div><span class="delete" data-cartid="'+product.id+'">删除</span></div>');
                });
            } else {
                products.addClass('hide');
                $('footer').addClass('hide');
            }
        }
    });

    function callWxPurchase(order_id, order) {
        WeixinJSBridge.invoke(
            'getBrandWCPayRequest', {
                appId: order.appId,
                timeStamp: order.timeStamp,
                nonceStr: order.nonceStr,
                package: order.package,
                signType: order.signType,
                paySign: order.sign
            },
            function(res){
                if (res.err_msg == "get_brand_wcpay_request:ok") {
                    showSuccessDialog("支付成功");
                    $('.products').empty();
                    $('.empty').removeClass('hide').text('您的购物车是空的，赶紧去添加吧！');
                    location.replace('/static/buy_success.html?order_id='+order_id);
                } else if (res.err_msg == "get_brand_wcpay_request:fail") {
                    showFailDialog("支付失败");
                }
            }
        );
    }

    function buyProduct(url){
        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog("购买成功");
                    $('.products').empty();
                    $('.empty').removeClass('hide').text('您的购物车是空的，赶紧去添加吧！');
                    location.replace('/static/buy_success.html?order_id='+order.id);
                } else if (result.code === 10006) {
                    var data = result.data.order;
                    var order_id = result.data.order_id;
                    callWxPurchase(order_id, data);
                } else {
                    showTips(result.msg);
                }
            }
        });
    }

    function showdialog() {
        $.dialog({
           type : 'confirm',
           titleText: '选择支付方式',
           buttonText: {
               ok: '使用优惠购买',
               cancel: '使用余额购买'
           },
           onClickOk : function(){
                buyProduct('/cart/pay_with_coupon');
           },
           onClickCancel : function(){
                buyProduct('/cart/pay_with_balance');
           },
           contentHtml : '<p>不能同时使用余额和优惠额度。</p><p>请选用余额或者优惠券中的一种方式进行支付, 不足部分将通过微信支付。</p>'
        });
     }

    $('.purchase').click(function () {
        $.ajax({
            url: '/cart/pay',
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog('购买成功');
                    $('.products').empty();
                    $('.empty').removeClass('hide').text('您的购物车是空的，赶紧去添加吧！');
                } else if (result.code === 10007) {
                    showdialog();
                } else if (result.code === 10006) {
                    var data = result.data.order;
                    callWxPurchase(data);
                } else {
                    showTips(result.msg);
                }
            }
        });
    });
    products.on('click', '.delete', function () {
        var m = $(this);
        $.ajax({
            url: '/cart/delete',
            type: 'post',
            dataType: 'json',
            data: {
                cart_id: m.data('cartid')
            },
            success: function (result) {
                if (result.code === 0) {
                    m.parents('.product').remove();
                    if (!products.children().length) {
                        $('.empty').removeClass('hide').text('您的购物车是空的，赶紧去添加吧！');
                    }
                    showSuccessDialog('删除成功');
                } else {
                    showTips(result.msg);
                }
            }
        });
    });
    products.on('click', '.product_num span', function () {
        var m = $(this), input = m.siblings('input'), val = parseInt(input.val(), 10);
        if (m.hasClass('minus')) {
            if (val < 2) return;
            val -= 1;
        }
        if (m.hasClass('plus')) {
            val += 1;
        }
        input.val(val);
        st && clearTimeout(st);
        st = setTimeout(function () {
            $.ajax({
                url: '/cart/update',
                type: 'post',
                dataType: 'json',
                data: {
                    cart_id: m.data('cartid'),
                    num: val
                },
                success: function (result) {
                    if (result.code !== 0) {
                        showTips(result.msg);
                    }
                }
            });
        }, 300);
    });
    products.on('change', '.product_num input', function () {
        var m = $(this), val = m.val();
        if (/^[1-9]\d*$/.test(val)) {
            m.data('num', val);
            val = parseInt(val, 10);
        } else {
            m.val(m.data('num'));
            return;
        }
        $.ajax({
            url: '/cart/update',
            type: 'post',
            dataType: 'json',
            data: {
                cart_id: m.data('cartid'),
                num: val
            },
            success: function (result) {
                if (result.code !== 0) {
                    showTips(result.msg);
                }
            }
        });
    });
});