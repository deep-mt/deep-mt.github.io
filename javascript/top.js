var OnButtonClick = function pagetop() {
	$('body,html').animate({scrollTop: 0},500);
	return false;
};
$(function(){
    var scroll = $(document).scrollTop();
    if (scroll < 1) {
    	$(".pagetop-img-box").hide();
    } else {
    	$(".pagetop-img-box").show();
    }

    $(window).scroll(function () {
    	showPageTop();
    });
    function showPageTop(type) {
        var scroll = $(document).scrollTop();
        if (scroll < 1) {
        	$(".pagetop-img-box").fadeOut();
        } else {
        	$(".pagetop-img-box").fadeIn();
        }    	
    }
});