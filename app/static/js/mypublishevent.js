/**
 * Created by wills on 16/9/17.
 */

    function deleteEvent(event_id) {
        $.ajax({
            url: '/user/event/'+event_id,
            type: 'delete',
            dataType: 'json',
            success: function(result) {
                if(result.code === 0) {
                    location.replace('/static/mypublishevent.html?a=d');
                } else {
                    showFailDialog(data.msg);
                }
            }
        });
    }

    function deleteClick(event_id){
        $.dialog({
           type : 'confirm',
           onClickOk : function(){
               deleteEvent(event_id);
           },
           contentHtml : '<p>确定删除活动?</p><p>删除后将无法恢复</p>'
        });
    }
$(function () {
    function getEvent(event) {
        return  '<div class="event"><div class="event-hd clear"><p class="fl">'+event.title+'</p></div><div class="event-bd"><img src="'+event.poster_url+'" alt=""/><span class="question">'+event.description.replace(/\r\n/g, "<br>")+'</span><p>费用：'+event.fee/100.0+'元</p><p>已报名：'+event.num+'人</p><p>开始时间：'+event.open_at+'</p><p>地点：'+getShopName(event.shop_id)+'</p></div><action><a href="event_info.html?event_id='+event.id+'">报名详情</a><a href="edit_event.html?event_id='+event.id+'">修改</a><a class="warn" onclick="deleteClick('+event.id+')">删除</a></action></div>';
	}
    var empty = $('.empty'), events = $('.events');
    var a = getUrlParam('a');
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
                if (a=='c') {
                    showSuccessDialog('创建成功');
                } else if (a=='e') {
                    showSuccessDialog('修改成功');
                } else if (a=='d') {
                    showSuccessDialog('删除成功');
                }
            } else {
                empty.removeClass('hide');
            }
        }
    });

});