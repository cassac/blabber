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
    $post_id = $('.title').attr('id');
    $formData = $('#blog-post-form').serializeArray();
    $.ajax($SCRIPT_ROOT + '/posts/' + $post_id, {
    type: "PUT",
    data: $formData,
    success: function(data){
        location.href = "/";
      // flashMessage('success', response);
    }, // end success
    error: function(error) {
        console.log('error', error)
       // flashMessage('danger', 'Error: post not deleted');
    }// end error
    }); // end ajax      
});

var loadPost = function(post_id) {
  $.ajax($SCRIPT_ROOT + '/posts/' + post_id, {
    type: "GET",
    success: function(data){
        $('.title').attr('id', post_id)
        $('.title').val( data.post[0].title );
        $('.content').val( data.post[0].content );
      // flashMessage('success', response);
    }, // end success
    error: function(error) {
        console.log('error', error)
       // flashMessage('danger', 'Error: post not deleted');
    }// end error
  }); // end ajax 
}

var submitEdit = function(post_id) {
  $formData = $('#blog-post-form').serializeArray();
  $.ajax($SCRIPT_ROOT + '/posts/' + post_id, {
    type: "PUT",
    data: $formData,
    success: function(data){
        console.log('successfully updated')
      // flashMessage('success', response);
    }, // end success
    error: function(error) {
        console.log('error', error)
       // flashMessage('danger', 'Error: post not deleted');
    }// end error
  }); // end ajax 
}
