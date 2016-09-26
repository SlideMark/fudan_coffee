/**
 * Created by irish on 16/9/17.
 */
$(function () {
    var empty = $('.empty'), products = $('.products'), st = 0;
   $.ajax({
        url: '/cart',
        type: 'get',
        dataType: 'json',
        success: function(result) {
            $('.loading').addClass('hide');
            if(result.data.length) {
                empty.addClass('hide');
                result.data.forEach(function(product) {
                    products.append('<div class="product"><a href="product.html?pid='+product.id+'"><img src="'+product.product_icon+'" /><div class="product_info"><p class="description">'+product.product_name+'</p><span class="price">价格：'+product.product_price/100+'元</span></div></a><div class="product_num"><span class="minus" data-cartid="'+product.id+'">-</span><input type="text" data-num="'+product.num+'" data-cartid="'+product.id+'" value="'+product.num+'" class="num" /><span data-cartid="'+product.id+'" class="plus">+</span></div><span class="delete" data-cartid="'+product.id+'">删除</span></div>');
                });
            } else {
                products.addClass('hide');
                $('footer').addClass('hide');
            }
        }
    });
    $.ajax({
        url: '/user',
        type: 'get',
        dataType: 'json',
        success: function (result) {
            if(result.user.coupon) {
                $('.coupon').removeClass('hide');
            }
        }
    });
    $('.purchase').click(function () {
        var tail = $(this).hasClass('cart') ? 'pay_with_balance' : 'pay_with_coupon';
        $.ajax({
            url: '/cart/'+tail,
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
    products.on('click', '.delete', function () {
        var m = $(this);
        $.ajax({
            url: '/cart/delete',
            type: 'post',
            dataType: 'json',
            data: {
                cart_id: m.data('cartid')
            },
            success: function (result) {
                if (result.code === 0) {
                    m.parents('.product').remove();
                    if (!products.children().length) {
                        $('.empty').removeClass('hide').text('您的购物车是空的，赶紧去添加吧！');
                    }
                    alert('删除成功');
                } else {
                    alert(result.msg);
                }
            }
        });
    });
    products.on('click', '.product_num span', function () {
        var m = $(this), input = m.siblings('input'), val = parseInt(input.val(), 10);
        if (m.hasClass('minus')) {
            if (val < 2) return;
            val -= 1;
        }
        if (m.hasClass('plus')) {
            val += 1;
        }
        input.val(val);
        st && clearTimeout(st);
        st = setTimeout(function () {
            $.ajax({
                url: '/cart/update',
                type: 'post',
                dataType: 'json',
                data: {
                    cart_id: m.data('cartid'),
                    num: val
                },
                success: function (result) {
                    if (result.code !== 0) {
                        alert(result.msg);
                    }
                }
            });
        }, 300);
    });
    products.on('change', '.product_num input', function () {
        var m = $(this), val = m.val();
        if (/^[1-9]\d*$/.test(val)) {
            m.data('num', val);
            val = parseInt(val, 10);
        } else {
            m.val(m.data('num'));
            return;
        }
        $.ajax({
            url: '/cart/update',
            type: 'post',
            dataType: 'json',
            data: {
                cart_id: m.data('cartid'),
                num: val
            },
            success: function (result) {
                if (result.code !== 0) {
                    alert(result.msg);
                }
            }
        });
    });
});