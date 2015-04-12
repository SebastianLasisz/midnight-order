/**
 * Created by Sedi on 2015-03-21.
 */

$(document).ready(function () {
    $("img").each(function () {
        var image = $(this);
        if (image.width() > 100) {
            $(this).replaceWith("<a class='fancybox' rel='group' href='" + $(this).attr("src") + "'>" + "<img src='" + $(this).attr("src") + "' style=width:100% />" + "</a>");
        }
    })
    $(".fancybox").fancybox();
});