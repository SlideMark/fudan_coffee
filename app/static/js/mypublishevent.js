/**
 * Created by wills on 16/9/17.
 */


$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><img src="'+event.poster_url+'" alt=""/><span class="question">'+event.description+'</span><p>费用：'+event.fee/100.0+'元</p><p>已报名：'+event.num+'人</p><p>开始时间：'+event.open_at+'</p><p>地点：'+getShopName(event.shop_id)+'</p></div><action><a href="event_info.html?event_id='+event.id+'">查看报名详情</a></action></div>';
	}
    var empty = $('.empty'), events = $('.events');
    $.ajax({
        url: '/user/events/publish',
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