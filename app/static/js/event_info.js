/**
 * Created by wills on 16/9/17.
 */

$(function () {
    var event_id = getUrlParam('event_id');
    function getUser(user) {
        return  '<div class="user"><div class="user-hd clear"><p class="fl">'+user.name+'</p><p class="fr">'+user.join_at+'</p></div>';
	}
    var empty = $('.empty');
    var users = $('.users');
    $.ajax({
        url: '/user/event/'+event_id,
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            var ev = result.data;
            if(ev.users.length) {
                empty.addClass('hide');
                ev.users.forEach(function(user) {
                    users.append(getUser(user));
                });
            } else {
                empty.removeClass('hide');
            }
        }
    });

});