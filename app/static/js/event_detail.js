/**
 * Created by wills on 16/9/17.
 */

$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><img src="'+event.poster_url+'" alt=""/><span class="question">'+event.description+'</span><hr><p>费用：'+event.fee/100.0+'元</p><hr><p>组织者：'+event.creator.name+'</p><hr><p>已报名：'+event.num+'人</p><hr><p>活动时间：'+event.open_at+'~'+event.close_at+'</p><hr><p>地点：'+getShopName(event.shop_id)+'</p></div></div>';
	}
    var event_id = getUrlParam('event_id');
    var event = $('.event');
    var footer = $('.join');
    var header = $('.header');
    $.ajax({
        url: '/event/'+event_id,
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            var ev = result.data;
            event.append(getEvent(ev));
            header.html(ev.title);
            if (ev.member === 1) {
                footer.html('已报名');
            } else {
                footer.click(function () {
                    join_event(event_id);
                });
            }
            wx.ready(function() {
                wx.onMenuShareTimeline({
                    title: ev.description,
                    link: location.href,
                    imgUrl: ev.poster_url,
                    success: function() {},
                    fail: function() {}
                });
                wx.onMenuShareAppMessage({
                    title: ev.title,
                    desc: ev.description,
                    link: location.href,
                    imgUrl: ev.poster_url,
                    success: function() {},
                    fail: function() {}
                });
            });
        }
    });
});