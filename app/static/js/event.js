/**
 * Created by wills on 16/9/17.
 */
$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><img href="'+event.poster_url+'"/><span class="question">'+event.description+'</span><p>费用：'+event.fee/100.0+'元</p><p>组织者：'+event.creator.name+'</p><p>开始时间：'+event.open_at+'</p><p>地点：'+'歌华大厦'+'</p></div></div>';
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
                $('footer').removeClass('hide');
                result.data.forEach(function(event) {
                    events.append(getEvent(event));
                });
            } else {
                empty.removeClass('hide');
                $('footer').addClass('hide');
            }
        }
    });
});