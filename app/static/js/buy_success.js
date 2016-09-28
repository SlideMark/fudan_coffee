/**
 * Created by wills on 16/9/17.
 */
$(function () {
    function getOrder(order) {
        var type = '';
        if (order.type === 0) {
            return  '<div class="order"><div class="order-hd clear"><p class="fl">充值成功：'+order.order_id+'</p></div><div class="order-bd"><span class="question">'+order.name+'</span><p>购买用户：'+order.user_name+'</p><p>微信扣费：'+order.money/100.0+'元</p><p>余额扣费：'+order.balance/100.0+'元</p><p>优惠扣费：'+order.coupon/100.0+'元</p><p>日期：'+order.create_at+'</p></div></div>';

        } else {
            return  '<div class="order"><div class="order-hd clear"><p class="fl">购买成功：'+order.order_id+'</p></div><div class="order-bd"><span class="question">'+order.name+'</span><p>购买用户：'+order.user_name+'</p><p>微信扣费：'+order.money/100.0+'元</p><p>余额增加：'+order.balance/100.0+'元</p><p>日期：'+order.create_at+'</p></div></div>';
        }
	}
    var order_view = $('.order');
    var order_id = getUrlParam('order_id');
    $.ajax({
        url: '/order/'+order_id,
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.code === 0) {
                var order = result.data;
                if (order.state != 1) {
                    showTips('订单无效!');
                } else {
                    order_view.append(getOrder(result.data));
                    showSuccessDialog('购买成功!');
                }
            } else {
                showTips(result.msg)
            }
        }
    });
});