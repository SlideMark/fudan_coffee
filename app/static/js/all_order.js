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
        return  '<div class="order"><div class="order-hd clear"><p class="fl">'+type+order.order_id+'</p><p class="fr">'+state+'</p></div><div class="order-bd"><span class="question">'+order.name+'</span><p>用户：'+order.user_name+'</p><p>微信：'+order.money/100.0+'元</p><p>余额：'+order.balance/100.0+'元</p><p>优惠：'+order.coupon/100.0+'元</p><p>日期：'+order.create_at+'</p></div></div>';
	}
    var empty = $('.empty'), orders = $('.orders');
    var maxId = 0;
    function getNewOrders() {
        var startTime = new Date().getTime();
        $.ajax({
            url: '/all_orders?max_id='+maxId,
            type: 'get',
            dataType: 'json',
            success: function(result) {
                $('.loading').addClass('hide');
                if(result.data.length) {
                    empty.addClass('hide');
                    $('footer').removeClass('hide');
                    result.data.forEach(function(order) {
                        if (order.id > maxId) {
                            maxId = order.id;
                        }
                        orders.prepend(getOrder(order));
                    });
                    showSuccessDialog('新的订单完成!');
                }
            }
        });
    }
    getNewOrders()

    setInterval(getNewOrders,5000)
});