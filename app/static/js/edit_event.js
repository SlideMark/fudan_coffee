/**
 * Created by irish on 16/9/14.
 */
$(function() {
    var event_id = getUrlParam('event_id');

    var title=$('.title'), desc=$('.description'), fee=$('.fee'), shop_id=$('.shop_id'),
        open_time=$('.open_at'), close_time=$('.close_at'), poster=$(".poster"), show_num=$(".show_num");
    var titleTip = $('.titleTip'), descTip = $('.descTip'), createTip = $('.createTip'),
        openTimeTip = $('.openTimeTip'), closeTimeTip = $('.closeTimeTip');
    var titleValidate = true, descValidate = true, openTimeValidate = true, closeTimeValidate = true;

    title.change(function () {
        titleValidate = $(this).val().length > 0;
        titleTip.text(titleValidate ? '' : '请输入标题');
    });
    desc.change(function () {
        descValidate = $(this).val().length > 0;
        descTip.text(descValidate ? '' : '请输入活动简介');
    });
    open_time.change(function () {
        openTimeValidate = $(this).val().length > 0;
        openTimeTip.text(openTimeValidate ? '' : '请选择活动开始时间');
    });
    close_time.change(function () {
        closeTimeValidate = $(this).val().length > 0;
        closeTimeTip.text(closeTimeValidate ? '' : '请选择活动结束时间');
    });


     $(".poster").change(function(e){
         var file = e.target.files||e.dataTransfer.files;
         if(file){
             var reader = new FileReader();
             reader.onload=function(){
                  $("#poster_img").attr("src", this.result);
             }
             reader.readAsDataURL(file[0]);
            }
      });

    $('#submit').click(function(e) {
        e.preventDefault();
        if(titleValidate && descValidate && openTimeValidate && closeTimeValidate) {
            var data = new FormData($('#create_form').get()[0]);
            showProcessDialog("提交中...");
            $.ajax({
                url: '/user/event/'+event_id,
                type: 'put',
                data: data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(data) {
                    if(data.code === 0) {
                        location.replace('/static/mypublishevent.html?a=e');
                    } else {
                        createTip.text(data.msg);
                    }
                }
            });
        } else {
            createTip.text('请完成填写');
        }
    });

    $.ajax({
        url: '/event/'+event_id,
        type: 'get',
        dataType: 'json',
        success: function(result) {
            var ev = result.data;
            title.val(ev.title);
            desc.val(ev.description);
            fee.val(ev.fee/100.0);
            $('input[type="radio"][name="shop_id"][value="'+ev.shop_id+'"]').attr("checked", "checked");
            if (ev.show_num) {
                show_num.attr("checked", "checked");
            }
            open_time.val(ev.open_at.split(" ").join("T"));
            close_time.val(ev.close_at.split(" ").join("T"));
            $("#poster_img").attr("src", ev.poster_url);
        }
    });
});