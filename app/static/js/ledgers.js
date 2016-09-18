/**
 * Created by irish on 16/9/18.
 */
$(function () {
    function getUrlParam(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
        return results == null  ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '))
    }
    var loading = $('.loading'), records = $('.records'), norecord = $('.norecord'), type = getUrlParam('type');
    $.ajax({
        url: '/ledgers',
        type: 'get',
        dataType: 'json',
        data: {
            type: type
        },
        success: function (result) {
            loading.addClass('hide');
            var data = result.data;
            if (data.length) {
                data.forEach(function(list) {
                    records.append('<a href="product.html?pid='+list.item_id+'"><span>'+list.name+'</span><span>'+list.money+'</span></a>');
                });
            } else {
                records.addClass('hide');
                norecord.text('没有'+ (type==0 ? '余额' : '优惠券')+'消费记录');
         }
            $('.avator').attr('src', user.avatar);
            $('.nickname').text(user.name);
            $('.balance span').text('￥'+user.balance/100.0+'元');
            $('.coupon span').text('￥'+user.coupon/100.0+'元');
        }
    });
});