/**
 * Created by irish on 16/9/14.
 */
$(function() {
    var phone = $('.phone'), password = $('.password'), confirmPassword = $('.confirmPassword'), signupTip = $('.signupTip'),
        phoneTip = $('.phoneTip'), pwdTip = $('.pwdTip'), conTip = $('.conTip'), phonevalidate = false, pwdvalidate = false, conpwdvalidate = false;
    phone.change(function () {
        phonevalidate = /^1(3|5|7|8)\d{9}$/.test($(this).val());
        phoneTip.text(phonevalidate ? '' : '手机号格式不正确');
    });
    password.change(function () {
        pwdvalidate = $(this).val().length > 5;
        pwdTip.text(pwdvalidate ? '' : '密码长度不能少于6位');
        if(confirmPassword.val() != '') {
            confirmPassword.trigger('change');
        }
    });
    confirmPassword.change(function () {
        conpwdvalidate = $(this).val() == password.val();
        conTip.text(conpwdvalidate ? '' : '两次输入密码不相符');
    });
    $('#submit').click(function(e) {
        e.preventDefault();
        if(phonevalidate && pwdvalidate && conpwdvalidate) {
            $.ajax({
                url: '/account/signup',
                type: 'post',
                dataType: 'json',
                data: {
                    phone: phone.val(),
                    password: password.val()
                },
                success: function(data) {
                    if(data.code === 0) {
                        location.replace('/static/index.html');
                    } else {
                        signupTip.text(data.msg);
                    }
                }
            });
        }
    });
});