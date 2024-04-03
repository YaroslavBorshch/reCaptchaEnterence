// custom_script.js
$(document).ready(function() {
    $('#username_enter_form').submit(function(e) {
        e.preventDefault();

        $('#loader').show();
        $('#result').hide();

        // Получаем CSRF токен из куков через Django тег
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '',
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                $('#result').show()
                $(`#response_code`).show().text(response.code);
                $('#response_message').show().text(response.message);
                if (response.code !== 200) {
                    $('#response_block_code').removeClass('alert-success').addClass('alert-danger');
                }
                else {
                    $('#response_block_code').removeClass('alert-danger').addClass('alert-success');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            },
            complete: function() {
                $('#loader').hide();
            },
        });
    });
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}