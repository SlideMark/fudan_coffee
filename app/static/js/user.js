/**
 * Created by irish on 16/9/18.
 */
$(function () {
    function getUrlParam(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
        return results == null  ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '))
    }
    var loading = $('.loading'), products = $('.products');
    $.ajax({
        url: '/user',
        type: 'get',
        dataType: 'json',
        success: function (result) {
            var user = result.user;
            $('.avator').attr('src', user.avatar);
            $('.nickname').text(user.name);
            $('.balance span').text('￥'+user.balance);
            $('.coupon span').text('￥'+user.coupon);
        }
    });
});