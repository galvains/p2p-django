$("#id_username").change(function() {
    let username = $(this).val();
    $.ajax({
        url: 'validate_login/',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function(data) {
            if (username && !data.is_taken) {
                $('#user_error').remove();
                $("#id_username").css('border-color', '#ff6666');
                $("#username").append('<div class="custom-errors-form" id="user_error">This user does not exist.</div>');
            } else {
                $("#id_username").css('border-color', '#c8c8c8');
                $('#user_error').remove();
            }
        }
    });
});