function wxCallBack(res) {
	wx.config({
		debug: true,
		appId: 'wxc21f8a22b8362d8b',
		timestamp:res.data.time_stamp,
		nonceStr: res.data.noncestr,
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