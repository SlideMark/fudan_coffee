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
