/**
 * Created by wills on 16/9/17.
 */
$(function () {
    function getOrder(order) {
        var type = '';
        if (order.type === 0) {
            type = '充值：';
        } else {
            type = '购买：';
        }
        var state = '';
        if (order.state === 0) {
            state = '未支付';
        } else if (order.state === 1) {
            state = '已完成';
        } else {
            state = '已取消';
        }
        return  '<div class="order"><div class="order-hd clear"><p class="fl">'+type+order.order_id+'</p><p class="fr">'+state+'</p></div><div class="order-bd"><span class="question">'+order.name+'</span><p>微信：'+order.money/100.0+'元</p><p>余额：'+order.balance/100.0+'元</p><p>优惠：'+order.coupon/100.0+'元</p><p>日期：'+order.create_at+'</p></div></div>';
	}
    var empty = $('.empty'), orders = $('.orders');
    $.ajax({
        url: '/orders',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                $('footer').removeClass('hide');
                result.data.forEach(function(order) {
                    orders.append(getOrder(order));
                });
            } else {
                orders.addClass('hide');
                empty.removeClass('hide');
                $('footer').addClass('hide');
            }
        }
    });
});