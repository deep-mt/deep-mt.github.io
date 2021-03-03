$(function() {


// PCページのみ適用
if ($('.pc-none').css('display') == 'none'){
	// ページタイトル取得
	var getPageTitle = $('.body-title').first().text()
	// 対象のタイトルのナビにボーダーを引く
	$('.menu-li a:contains('+getPageTitle+')').css('border-bottom', 'solid 3px #87CEFA');
	$('.menu-li a:contains('+getPageTitle+')').css('padding-bottom', '13px');
}

//メニュークリック時
$('.menu-trigger').click(function(){

	//menu-triggerのactiveクラスが要素に無ければ追加し、あれば削除する。
	$(this).toggleClass('active');

	        if ($(this).hasClass('active')) {
	        	// alert("ナビをアクティブ");
            $('.globalMenuSp').addClass('active');
        } else {
        	// alert("ナビを隠す");
            $('.globalMenuSp').removeClass('active');
        }

});


});
