/**
 * Created by irish on 16/9/17.
 */
$(function () {
    var empty = $('.empty'), payments = $('.payments'), st = 0;
    $.ajax({
        url: '/payment_items',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                result.data.forEach(function(payment) {
                    payments.append('<div class="payment"><div class="payment_info"><p class="description">'+payment.name+'</p><span class="price">价格：'+payment.money/100.0+'元, 返现'+payment.charge/100.0+'元</span></div><span class="buy" data-paymentitemid="'+payment.id+'">购买</span></div>');
                });
            } else {
                payments.addClass('hide');
                $('footer').addClass('hide');
            }
        }
    });

    payments.on('click', '.buy', function () {
        var m = $(this);
        $.ajax({
            url: '/payment_order?item_id='+m.data('paymentitemid'),
            type: 'get',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    var order = result.data;
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
                            if(res.err_msg == "get_brand_wcpay_request：ok" ) {
                                location.replace('/static/cart.html?t='+new Date().getTime());
                                showSuccessDialog("支付成功");
                            }
                        }
                    );
                } else {
                    showTips(result.msg);
                }
            }
        });
    });
});