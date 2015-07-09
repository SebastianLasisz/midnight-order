/**
 * Created by Sedi on 2015-03-21.
 */

$(document).ready(function () {
    $("img").each(function () {
        var image = $(this);
        if (image.width() > 100) {
            image.wrap("<a href='" +image.attr('src')+ "' class='fancybox' rel='group'></a>");
        }
    })
    $(".fancybox").fancybox();
});