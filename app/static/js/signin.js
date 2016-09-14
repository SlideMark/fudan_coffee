/**
 * Created by irish on 16/9/14.
 */
$(function() {
    var phone = $('.phone'), password = $('.password'), signinTip = $('.signinTip'),
        phoneTip = $('.phoneTip'), pwdTip = $('.pwdTip'), phonevalidate = false, pwdvalidate = false;
    phone.change(function () {
        phonevalidate = /^1(3|5|7|8)\d{9}$/.test($(this).val());
        phoneTip.text(phonevalidate ? '' : '手机号格式不正确');
    });
    password.change(function () {
        pwdvalidate = $(this).val().length > 5;
        pwdTip.text(pwdvalidate ? '' : '密码长度不能少于6位');
    });
    $('#submit').click(function(e) {
        e.preventDefault();
        if(phonevalidate && pwdvalidate) {
            $.ajax({
                url: '/account/login',
                type: 'post',
                dataType: 'json',
                data: {
                    phone: phone.val(),
                    password: password.val()
                },
                success: function(data) {
                    if(data.code === 0 || data.code === 10001) {
                        location.replace('/static/index.html');
                    } else {
                        signinTip.text(data.msg);
                    }
                }
            });
        }
    });
});