/**
 * Created by wills on 16/9/17.
 */
$(function () {
    function getOrder(order) {
        var type = '';
        if (order.type === 0) {
            type = '充值';
        } else {
            type = '购买';
        }

        var state = '';
        if (order.state === 0) {
            state = '未支付';
        } else if (order.state === 1) {
            state = '已完成';
        } else {
            state = '已取消';
        }
        return  '<div class="title">'+
                    '<div style="height:30px;border-bottom:1px solid #efefef;margin-left:5px;color:#444349;">'+
                        '<li style="margin-left:5px;float:left;">'+type+':&nbsp'+order.order_id+'<li>'+
                        '<li class="state" style="float:right;margin-right:10px;">'+state+'</li>'+
                    '</div>'+
				    '<div style="height:28px;margin-top:13px;margin-left:5px;font-size:16px;">'+
			            '<span class="question">'+order.name+'</span>'+
			        '</div>'+
				    '<div style="margin-left:10px;color:#838184">'+
			            '<p>微信:&nbsp'+order.money/100.0+'元</p>'+
			            '<p>余额:&nbsp'+order.balance/100.0+'元</p>'+
			            '<p>优惠:&nbsp'+order.coupon/100.0+'元</p>'+
			        '</div>'+
				    '<div style="margin-left:10px;color:#838184;margin-top:5px;">'+
				        '<p>日期:&nbsp'+order.create_at+'</p>'+
				    '</div>'+
				 '</div>';
	}

    var empty = $('.empty'), orders = $('.orders'), st = 0;
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
                $('footer').addClass('hide');
            }
        }
    });
});