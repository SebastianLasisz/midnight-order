//Changing CSS files
$(document).ready(function() {
	$("#nav li a").click(function() {
		$("link").attr("href",$(this).attr('rel'));
		return false;
	});
});

$("link.changeme").attr("href",$(this).attr('rel'));

$(document).ready(function() {
	if($.cookie("css")) {
		$("link").attr("href",$.cookie("css"));
	}
	$("#nav li a").click(function() {
		$("link").attr("href",$(this).attr('rel'));
		$.cookie("css",$(this).attr('rel'), {expires: 365, path: '/'});
		return false;
	});
});