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
                    alert('成功加入购物车');
                }
            }
        });
    });
    $('.purchase').click(function () {
        var tail = $(this).hasClass('buy') ? 'with_balance' : 'with_coupon';
        $.ajax({
            url: '/product/'+pid+'/'+tail,
            type: 'post',
            dataType: 'json',
            success: function (result) {
                if (result.code === 0) {
                    alert('购买成功')
                } else if (result.code === 10006) {
                    var data = result.data.order;
                    WeixinJSBridge.invoke(
				       'getBrandWCPayRequest', {
				           appId: data.appId,
				           timeStamp: data.timeStamp,
				           nonceStr: data.nonceStr,
				           package: data.package,
				           signType: data.signType,
				           paySign: data.sign
				       },
				       function(res){
				       		alert(JSON.stringify(res));
				       }
				    );
                } else {
                    alert(result.msg);
                }
            }
        });
    });
});