/**
 * Created by wills on 16/9/17.
 */
$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><p>支付：'+event.fee/100.0+'元</p><p>开始日期：'+event.open_at+'</p><p>报名日期：'+event.join_at+'</p></div></div>';
	}
    var empty = $('.empty'), events = $('.events');
    $.ajax({
        url: '/user_events',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                $('footer').removeClass('hide');
                result.data.forEach(function(event) {
                    events.append(getEvent(event));
                });
            } else {
                events.addClass('hide');
                empty.removeClass('hide');
                $('footer').addClass('hide');
            }
        }
    });
});