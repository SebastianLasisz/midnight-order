/**
 * Created by Sedi on 2015-03-21.
 */

var counter = "{{messages_inbox_count}}";
$(document).ready(function () {
    auto_refresh();
});
function auto_refresh() {
    $.ajax({
        url: 'http://127.0.0.1:8000/ajax_test',
        type: 'get',
        success: function (data) {
            alert(counter)
            if (data != counter)
                alert(data);
            counter = data;
        }
    });
}
var refreshId = setInterval(auto_refresh, 20000);