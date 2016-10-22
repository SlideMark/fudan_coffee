/**
 * Created by irish on 16/9/14.
 */
$(function() {
    var title=$('.title'), desc=$('.description'), fee=$('.fee'),
        open_time=$('.open_at'), close_time=$('.close_at'), poster=$(".poster");
    var titleTip = $('.titleTip'), descTip = $('.descTip'), createTip = $('.createTip'),
        openTimeTip = $('.openTimeTip'), closeTimeTip = $('.closeTimeTip');
    var titleValidate = false, descValidate = false, openTimeValidate = false, closeTimeValidate = false;
    var create_form = $('#create_form');

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
                  $("#poster_img").attr("width", "320");
                  $("#poster_img").attr("height", "300");
             }
             reader.readAsDataURL(file[0]);
            }
      });

    create_form.submit(function(e) {
        e.preventDefault();
        if(titleValidate && descValidate && openTimeValidate && closeTimeValidate) {
            $('.modal').show();
            var data = new FormData(create_form.get()[0]);
            $.ajax({
                url: '/event',
                type: 'post',
                data: data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                beforeSend:function () {
                    $('.modal').show();
                },
                complete:function(){
                    $('.modal').hide();
                },
                success: function(data) {
                    if(data.code === 0) {
                        location.replace('/static/mypublishevent.html?a=c');
                    } else {
                        createTip.text(data.msg);
                    }
                }
            });
        } else {
            createTip.text('请完成填写');
        }
    });
});