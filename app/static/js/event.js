/**
 * Created by wills on 16/9/17.
 */
$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><img src="'+event.poster_url+'" alt=""/><span class="question">'+event.description+'</span><p>费用：'+event.fee/100.0+'元</p><p>组织者：'+event.creator.name+'</p><p>开始时间：'+event.open_at+'</p><p>地点：'+'歌华大厦'+'</p></div><action><a href="">我要报名</></action></div>';
	}
    var empty = $('.empty'), events = $('.events');
    $.ajax({
        url: '/events',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                result.data.forEach(function(event) {
                    events.append(getEvent(event));
                });
            } else {
                empty.removeClass('hide');
            }
        }
    });

    function join(event_id) {
        $.ajax({
            url: '/event/event_id',
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog('报名成功');
                } else if (result.code === 10006) {
                    var order = result.data.order;
                    var order_id = result.data.order_id;
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
                                location.replace('/static/buy_success.html?order_id='+order_id);
                            } else if (res.err_msg == "get_brand_wcpay_request:fail") {
                                showFailDialog("支付失败");
                            }
                        }
                    );
                } else {
                    showTips(result.msg);
                }
            }
        });
    }
});