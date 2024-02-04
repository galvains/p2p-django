    $("#id_username").change(function () {
        let username = $(this).val();

        $.ajax({
            url: 'validate_username',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (username && (data.is_taken || data.valid_symbol)) {
                    $('#user_error').remove();
                    $("#id_username").css('border-color', '#ff6666');
                    if (data.is_taken) {
                        $("#username").append(
                        '<div class="errors-form" id="user_error">A user with that username already exists.</div>');
                    }
                    else {
                        $("#username").append(
                        '<div class="errors-form" id="user_error">Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.</div>');
                    }
                }
                else {
                    $("#id_username").css('border-color', '#c8c8c8');
                    $('#user_error').remove();
                }
            }
        });
    });

    $("#id_email").change(function () {
        let email = $(this).val();
        $.ajax({
            url: 'validate_email',
            data: {
                'email': email
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken && email) {
                    $('#email_error').remove();
                    $("#id_email").css('border-color', '#ff6666');
                    $("#email").append('<div class="errors-form" id="email_error">A user with that email already exists.</div>');
                }
                else {
                    $("#id_email").css('border-color', '#c8c8c8');
                    $('#email_error').remove();
                }
            }
        });
    });


    function toggleButton()
    {
        let username = $('#id_username').val();
        let email = $('#id_email').val();
        let password1 = $('#id_password1').val();
        let password2 = $('#id_password2').val();

        if (username && email && password1 && password2) {

            setTimeout(function(){
                if (counterErrors()){
                    $('#submitButton').attr('disabled', false);
                }
            }, 200);

        } else {
            $('#submitButton').attr('disabled', true);
        }
    }

    function counterErrors()
    {
        let errorsCount = $('.errors-form').length;
        return errorsCount == 0;
    }