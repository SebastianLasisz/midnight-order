if($.cookie("css")) {
    $("link").attr("href",$.cookie("css"));
}

$(document).ready(function() {
    $("#nav li a").click(function() {
        $("link").attr("href",$(this).attr('rel'));
        $.cookie("css",$(this).attr('rel'), {expires: 365, path: '/'});
        return false;
    });
});

