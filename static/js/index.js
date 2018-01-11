

$('#contact').on('submit',function(e){
        e.preventDefault();
        $.ajax({
            url: '/addComment',
            method: 'POST',
            data: $(this).serialize(),
            dataType: "json",
            success: function(res){
                $('input[name="name"]').val("");
                $('input[name="email"]').val("");
                $('input[name="phone_number"]').val("");
                $('textarea[name="message"]').val("");
                $.notify("Feedback Submitted", "success");
            },
            error: function(res){
                $.notify("Feedback Not Submitted", "error");
            }
        })
    });
