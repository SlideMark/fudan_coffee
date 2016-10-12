/**
 * Created by wills on 16/9/14.
 */
     function getUrlParam(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
        return results == null  ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '))
    }

    function getShopName(code) {
        if (code === 0){
            return '自由而无用歌华大厦店';
        }
        return '自由而无用奥体中心店';
    }

    function showSuccessDialog(msg) {
        $.dialog({
            type : 'info',
            infoText : msg,
            infoIcon : 'img/icon/success.png',
            autoClose : 2500
        });
    }
     function showFailDialog(msg) {
        $.dialog({
            type : 'info',
            infoText : msg,
            infoIcon : 'img/icon/fail.png',
            autoClose : 2500
        });
    }

    function showTips(msg) {
        $.dialog({
            type : 'tips',
            infoText : msg,
            autoClose : 2500
        });
    }


 function join_event(event_id) {
        $.ajax({
            url: '/event/'+event_id+'/join',
            type: 'get',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog('报名成功');
                } else if (result.code === 10003) {
                    var join = encodeURIComponent('http://'+location.host+'/event/'+event_id+'/join');
                    var url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc21f8a22b8362d8b&redirect_uri='+join+'&response_type=code&scope=snsapi_userinfo&state=';
                    //showTips('请关注自由而无用服务号进行报名');
                    location.replace(url);
                } else if (result.code === 10006) {
                    var order = result.data.order;
                    var order_id = result.data.order_id;
                    WeixinJSBridge.invoke(
                        'getBrandWCPayRequest', {
                            appId: order.appId,
                            timeStamp: order.timeStamp,
                            nonceStr: order.nonceStr,
                            package: order.package,
                            signType: order.signType,
                            paySign: order.sign
                        },
                        function(res){
                            if (res.err_msg == "get_brand_wcpay_request:ok") {
                                location.replace('/static/buy_success.html?order_id='+order_id);
                            } else if (res.err_msg == "get_brand_wcpay_request:fail") {
                                showFailDialog("支付失败");
                            }
                        }
                    );
                } else {
                    showTips(result.msg);
                }
            }
        });
 }
