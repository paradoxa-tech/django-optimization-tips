
function table_callback(csrf_token){
    $.ajax({
        "url": "/table_callback/",
        "type": "POST",
        "data": {
            "csrfmiddlewaretoken": csrf_token,
        },
        "success": function(result) {
            $("span#queries").html(result['queries']);
            $("span#time").html(result['time'] + ' seconds');
        }
    });
}
