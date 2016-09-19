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
            url: '/payment_order',
            type: 'post',
            dataType: 'json',
            data: {
                item_id: m.data('paymentitemid')
            },
            success: function (result) {
                if (result.code === 0) {
                    var data = result.data.order;
                    WeixinJSBridge.invoke(
				       'getBrandWCPayRequest', {
				           appId: data.appId,
				           timeStamp: data.timeStamp,
				           nonceStr: data.nonceStr,
				           package: data.package,
				           signType: data.signType,
				           paySign: data.sign
				       },
				       function(res){
				       		alert(JSON.stringify(res));
				       }
				    );
                } else {
                    alert(result.msg);
                }
            }
        });
    });
});