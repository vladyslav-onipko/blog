$(document).ready(function () {
    $('#id_email').on('blur', validate);

    function validate() {

        let email = $('#id_email').val();
        $.ajax({
           method: 'GET',
            url: '/user/registration/',
            data: {
               'email': email
            },
            dataType: 'json',
            success: function (data) {
               console.log(data);
               if (data.is_taken) {
                    $('#error-email').text(data.is_taken);
                    $('#btn').attr('disabled', 'disabled');
               } else {
                    console.log(1);
                    $('#btn').removeAttr('disabled');
               }
            },
            error: function (data) {
               console.log(data);
            }
        })
    }
})