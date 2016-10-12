/**
 * Created by wills on 16/9/17.
 */

$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><p>费用：'+event.fee/100.0+'元</p><p>组织者：'+event.creator.name+'</p><p>已报名：'+event.num+'人</p><p>开始时间：'+event.open_at+'</p><p>地点：'+getShopName(event.shop_id)+'</p></div><action><a href="/static/event_detail.html?event_id='+event.id+'">我要报名</></action></div>';
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

});