/**
 * Created by wills on 16/9/17.
 */

$(function () {
    function getEvent(event) {
        var r = '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><img src="'+event.poster_url+'" alt=""/><hr><p>介绍: '+event.description+'</p><hr><p>费用：'+event.fee/100.0+'元</p><hr><p>组织者：'+event.creator.name+'</p>';
        if (event.show_num) {
            r += '<hr><p>已报名：'+event.num+'人</p>';
        }
        r += '<hr><p>活动时间：'+event.open_at+'~'+event.close_at+'</p><hr><p>地点：'+getShopName(event.shop_id)+'</p></div></div>';
	    return r;
	}
    var event_id = getUrlParam('event_id');
    var code = getUrlParam('code');

    var event = $('.event');
    var footer = $('.join');
    var header = $('.header');
    $.ajax({
        url: '/event/'+event_id+'?code='+code,
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
                if (code.length != 0) {
                    join_event(event_id);
                }
                footer.click(function () {
                    join_event(event_id);
                });
            }
            wx.ready(function() {
                wx.onMenuShareTimeline({
                    title: ev.description,
                    link: location.href.split('&')[0],
                    imgUrl: ev.poster_url,
                    success: function() {},
                    fail: function() {}
                });
                wx.onMenuShareAppMessage({
                    title: ev.title,
                    desc: ev.description,
                    link: location.href.split('&')[0],
                    imgUrl: ev.poster_url,
                    success: function() {},
                    fail: function() {}
                });
            });
        }
    });
});