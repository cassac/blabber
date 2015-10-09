$('#blog-post-form').bootstrapValidator({
    // live: 'enabled',
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        title: {
            validators: {
                notEmpty: {
                    message: 'The Title is required and cannot be empty'
                }
            }
        },
        tag: {
            validators: {
                notEmpty: {
                    message: 'At least one tag is required'
                },
            }
        },
        content: {
            validators: {
                notEmpty: {
                    message: 'The content of a post cannot be empty'
                }
            }
        }
    }
})
.on('success.form.bv', function(e){
    e.preventDefault();
    $formData = $('#blog-post-form').serializeArray();
    $.ajax({
      url: "/posts",
      type: "POST",
      data: $formData,
      success: function(data){
           location.href = "/"
      },
      error: function(){
        alert("Failure: post was not created.");
      }
    });//close ajax        
});
