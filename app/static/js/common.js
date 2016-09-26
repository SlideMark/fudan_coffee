/**
 * Created by wills on 16/9/14.
 */
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

    function callWxPurchase(order) {
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
                    showSuccessDialog("支付成功");
            }
        );
    }

    function buyProduct(url){
        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog("购买成功");
                } else if (result.code === 10006) {
                    var data = result.data.order;
                    callWxPurchase(data);
                } else {
                    showTips(result.msg);
                }
            }
        });
    }
    function buyProductWithBalance(product_id) {
        buyProduct('/product/'+product_id+'/with_balance');
    }
    function buyProductWithCoupon(product_id) {
        buyProduct('/product/'+product_id+'/with_coupon');
    }

    function payCartWithBalance() {
        buyProduct('/cart/pay_with_balance');
    }
    function payCartWithCoupon() {
        buyProduct('/cart/pay_with_coupon');
    }