$("#id_username").change(function() {
    let username = $(this).val();
    $.ajax({
        url: 'validate_username/',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function(data) {
            if (username && (data.is_taken || data.valid_symbol)) {
                $('#user_error').remove();
                $("#id_username").css('border-color', '#ff6666');
                if (data.is_taken) {
                    $("#username").append('<div class="custom-errors-form" id="user_error">A user with that username already exists.</div>');
                } else {
                    $("#username").append('<div class="custom-errors-form" id="user_error">Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.</div>');
                }
            } else {
                $("#id_username").css('border-color', '#c8c8c8');
                $('#user_error').remove();
            }
        },
    });
});
$("#id_email").change(function() {
    let email = $(this).val();
    $.ajax({
        url: 'validate_email/',
        data: {
            'email': email
        },
        dataType: 'json',
        success: function(data) {
            if (data.is_taken && email) {
                $('#email_error').remove();
                $("#id_email").css('border-color', '#ff6666');
                $("#email").append('<div class="custom-errors-form" id="email_error">A user with that email already exists.</div>');
            } else {
                $("#id_email").css('border-color', '#c8c8c8');
                $('#email_error').remove();
            }
        }
    });
});

$("#id_password2, #id_password1").change(function() {
    let password1 = $('#id_password1').val();
    let password2 = $('#id_password2').val();
    $.ajax({
        url: 'validate_password/',
        data: {
            'password1': password1,
            'password2': password2,
        },
        dataType: 'json',
        success: function(data) {
            if (!data.is_similar || !data.is_length || !data.is_digits) {
                $("#id_password2").css('border-color', '#ff6666');
            }
            if (!data.is_length){
                $('#password_error_short').remove();
                $("#password2").append('<div class="custom-errors-form" id="password_error_short">This password is too short.</div>');

            }
            if (!data.is_similar) {
                $('#password_error_similar').remove();
                $("#password2").append('<div class="custom-errors-form" id="password_error_similar">The two password fields didn’t match.</div>');

            }
            if (!data.is_digits) {
                $('#password_error_digits').remove();
                $("#password2").append('<div class="custom-errors-form" id="password_error_digits">This password is entirely numeric.</div>');
            }
            if (data.is_similar && data.is_length && data.is_digits) {
                $("#id_password2").css('border-color', '#c8c8c8');
                $('#password_error_digits').remove();
                $('#password_error_similar').remove();
                $('#password_error_short').remove();
            }
        }
    });
});


function toggleButton() {
    let username = $('#id_username').val();
    let email = $('#id_email').val();
    let password1 = $('#id_password1').val();
    let password2 = $('#id_password2').val();

    if (username && email && password1 && password2 && captcha) {
        setTimeout(function() {
            if (counterErrors()) {
                $('#submitButton').attr('disabled', false);
            }
        }, 200);
    } else {
        $('#submitButton').attr('disabled', true);
    }
}

function counterErrors() {
    let errorsCount = $('.custom-errors-form').length;
    return errorsCount == 0;
}