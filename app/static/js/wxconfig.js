function wxCallBack(res) {
	wx.config({
		debug: false,
		appId: res.data.appId,
		timestamp:res.data.timestamp,
		nonceStr: res.data.nonceStr,
		signature:res.data.signature,
		jsApiList: [
			'checkJsApi',
			'onMenuShareTimeline',
			'onMenuShareAppMessage',
			'onMenuShareQQ',
			'onMenuShareQZone',
			'chooseImage',
			'previewImage',
			'uploadImage',
			'downloadImage',
			'translateVoice',
			'startRecord',
			'stopRecord',
			'onVoiceRecordEnd',
			'playVoice',
			'onVoicePlayEnd',
			'pauseVoice',
			'stopVoice',
			'uploadVoice',
			'downloadVoice',
			'openLocation',
			'getLocation'
		]
	});
}
$.ajax({
	url: '/signature',
	type: 'get',
	dataType: 'json',
	data: {
		url: location.href.split('#')[0]
	},
	success: function(res) {
		wxCallBack(res);
	}
});