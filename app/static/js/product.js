/**
 * Created by irish on 16/9/17.
 */
function getUrlParam(name) {
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
    return results == null  ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '))
}
$(function () {
    var pid = getUrlParam('pid');
    function getproduct() {
        $.ajax({
            url: '/product/'+getUrlParam('pid'),
            type: 'get',
            dataType: 'json',
            success: function (result) {
                document.title = result.data.name;
                $('.loading').addClass('hide');
                $('.product_imgs').attr('src', result.data.icon);
                $('.product_name').text(result.data.name);
                $('.product_des').text(result.data.description);
                $('.price').text('￥'+result.data.price/100.0+'元');
            }
        });
    }
    $.ajax({
        url: '/user',
        type: 'get',
        dataType: 'json',
        success: function (result) {
            getproduct();
            if(result.user.coupon) {
                $('.coupon').removeClass('hide');
            }
        }
    });
    $('.cart').click(function () {
        $.ajax({
            url: '/cart',
            type: 'post',
            dataType: 'json',
            data: {
                product_id: pid
            },
            success: function(result) {
                if(result.code === 0) {
                    showSuccessDialog('成功加入购物车');
                }
            }
        });
    });


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

    function showdialog(pid) {
        $.dialog({
           type : 'confirm',
           titleText: '选择支付方式',
           buttonText: {
               ok: '使用优惠购买',
               cancel: '使用余额购买'
           },
           onClickOk : function(){
                buyProduct('/product'+pid+'/with_balance');
           },
           onClickCancel : function(){
                buyProduct('/product'+pid+'/with_coupon');
           },
           contentHtml : '<p>不能同时使用余额和优惠额度。</p><p>请选用余额或者优惠券中的一种方式进行支付, 不足部分将通过微信支付。</p>'
        });
     }

    $('.purchase').click(function () {
        $.ajax({
            url: '/product/'+pid,
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    showSuccessDialog('购买成功');
                } else if (result.code === 10007) {
                    showdialog(pid);
                } else if (result.code === 10006) {
                    var data = result.data.order;
                    callWxPurchase(data);
                } else {
                    showTips(result.msg);
                }
            }
        });
    });
});