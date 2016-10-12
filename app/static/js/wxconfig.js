function wxCallBack(res) {
	wx.config({
		debug: true,
		appId: res.appId,
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
		url: location.href.split('#')[0].replace('&', '%26')
	},
	success: function(res) {
		wxCallBack(res);
	}
});