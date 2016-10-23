/**
 * Created by irish on 16/9/18.
 */
$(function () {
    var loading = $('.loading');
    var all_order = $('.all_order');
    $.ajax({
        url: '/user',
        type: 'get',
        dataType: 'json',
        success: function (result) {
            loading.addClass('hide');
            $('footer').removeClass('hide');
            var user = result.user;
            $('.avator').attr('src', user.avatar);
            $('.nickname').text(user.name);
            $('.balance span').text('￥'+user.balance/100);
            $('.coupon span').text('￥'+user.coupon/100);
            if (user.phone) {
                $('.bindphone').text('绑定手机号(已绑定)');
                $('.bindphone').removeAttr('href');
            }
            if (user.role && 4) {
                all_order.removeAttr('style');
            }
        }
    });
});