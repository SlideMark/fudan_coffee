/**
 * Created by irish on 16/9/14.
 */
$(function() {
    var phone = $('.phone'), password = $('.password'), confirmPassword = $('.confirmPassword'),
        phoneTip = $('.phoneTip'), pwdTip = $('.pwdTip'), conTip = $('.conTip');
    phone.change(function () {
        phoneTip.text(/^1(3|5|7|8)\d{9}$/.test($(this).value()) ? '' : '手机号格式不正确');
    });
    password.change(function () {
        // pwdTip.text()
    })
    $('#submit').click(function() {

    });
});