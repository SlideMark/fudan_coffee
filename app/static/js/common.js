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
            return '歌华大厦店';
        }
        return '奥体中心点';
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
