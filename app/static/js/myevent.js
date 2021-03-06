/**
 * Created by wills on 16/9/17.
 */

 var empty = $('.empty'), events = $('.events');

 function getEvent(event) {
     return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><p>支付金额：'+event.fee/100.0+'元</p><p>活动地点：'+getShopName(event.shop_id)+'</p><p>开始日期：'+event.open_at+'</p><p>报名日期：'+event.join_at+'</p></div><action><a onclick="leave_event('+event.id+');">取消报名</a></action></div>';
 }

 function load_event() {
     $.ajax({
        url: '/user/events/join',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            events.empty();
            if(result.data.length) {
                empty.addClass('hide');
                result.data.forEach(function(event) {
                    events.append(getEvent(event));
                });
            } else {
                events.addClass('hide');
                empty.removeClass('hide');
            }
        }
    });
 }
 function leave_event(event_id) {
        $.ajax({
            url: '/event/'+event_id+'/cancel',
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog('取消成功');
                    load_event();
                } else {
                    showTips(result.msg);
                }
            }
        });
 }

$(function () {
    load_event()
});