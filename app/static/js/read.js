var appendPost = function(post) {
  $post_div = '<div id="'+ post.id +'" class="parentDiv col-sm-12 col-xs-12 col-md-4 col-lg-4">' +
    '<div class="well">' +
        '<div class="media">' +
          '<a class="pull-left" href="#">' +
            '<img class="#">' +
          '</a>' +
        '<div class="media-body">'+
          '<h4 class="media-heading">'+ post.title +'</h4>' +
            '<p>' + post.content.slice(0, 100) + '...</p>' +
            '<h4><span style="cursor:pointer" class="readMore label label-default">Read More</span></h4>' +
            '<ul class="list-inline list-unstyled">' +
          '<li><span><i class="glyphicon glyphicon-calendar"></i> ' +
             moment( post.created ).format('YYYY-MM-DD') +
              '</span></li>' +
              '<li>|</li>' +
              '<span><i class="glyphicon glyphicon-user"></i> ' + post.author + '</span>' +
              '<li>|</li>' +
              '<li>' +
                 '<span class="likeBtn glyphicon glyphicon-star-empty"></span>' +
              '</li>' +
        '</ul>' +
         '</div>' +
      '</div>' +
    '</div>' +
  '</div>';
  $('#posts').append($post_div);
}; // end appendPost function

var appendLink = function(page, current_page) {
  var link = ''; 
  if (page==current_page) {
    link = '<li class="active"><a href="#">'+ current_page +'</a></li>';
  } else if ( page==null ){
   // do nothing if null 
  } else {
    link = '<li><a href="#">' + page + '</a></li>';
  }

  $('#pagination').append(link + '&#09;');
}

var likePost = function(post_id, status) {
  $postDiv = $('#'+post_id);
  $likeSpan = $postDiv.find('.likeBtn');

  if (status == 0) {
    $likeSpan.removeClass();
    $likeSpan.addClass('likeBtn glyphicon glyphicon-star-empty');
  } else {
    $likeSpan.removeClass();
    $likeSpan.addClass('likeBtn glyphicon glyphicon-star')
  }
}

var flashMessage = function(type, message) {
  $('.flashedMessage').remove()
  $flash_div = '<div class="flashedMessage col-md-offset-4 col-md-4 alert alert-'+ type +'">' +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +       
        message +
    '</div><div class="clearfix"></div>';
  $('#posts').prepend($flash_div);
} // end flashMessage
 
$(document).on('click', '.deleteBtn', function(event){
  $postDiv = $( this ).closest('.parentDiv');
  $postId = $postDiv.attr('id');
  $.ajax($SCRIPT_ROOT + '/posts/' + $postId, {
    type: "DELETE",
    success: function(response){
      $postDiv.remove();
      flashMessage('success', response);
    }, // end success
    error: function() {
       flashMessage('danger', 'Error: post not deleted');
    }// end error
  }); // end ajax  
}); // end on

$(document).on('click', '.likeBtn', function(event){
  $postDiv = $( this ).closest('.parentDiv');
  $postId = $postDiv.attr('id');
  csrftoken = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken)
          }
      }
  })
  $.ajax({
    url: "/like",
    type: "POST",
    data: {'post_id': $postId},
    success: function(data){
      likePost(data.post_id, data.like_status)
      flashMessage('success', data.message);
    }, // end success
    error: function(error) {
      console.log(error);
       flashMessage('danger', 'Error: post not liked');
    }// end error
  }); // end ajax  
}); // end on 

$(document).on('click', '#pagination a', function(event){
  $pageNum = $(this).text();
  fetchPosts($pageNum);
})

var fetchPosts = function(page) {
  var page_num;
  if (isNaN(page)) {
    page_num=1;
  } else {
    page_num=page;
  }
  $.ajax({
    url: '/posts', 
    type: "GET",
    data: {'page_num': page_num},
    success: function(response){
      $('#posts').empty();
      $('#pagination').empty();
      $.each(response.pages, function(index, pageNum){
        appendLink(pageNum, response.current_page);
      })
      $.each(response.posts, function(index, post){
        appendPost(post);
        likePost(post.id, post.like_status);
      }) // end function
    }, // end success
    error: function(error) {
       console.log("Error: ", error);
    } // end error
  }); // end ajax
}

var loadPost = function(post_id) {
  $.ajax($SCRIPT_ROOT + '/posts/' + post_id, {
    type: "GET",
    success: function(data){
      $postCreated = moment( data.post[0].created ).format('dddd, MMMM Do YYYY');
      $('#postTitle').text( data.post[0].title );
      $('#postAuthor').text( data.post[0].author );
      $('#postContent').text( data.post[0].content );
      $('#postCreated').text( $postCreated );
      // flashMessage('success', response);
    }, // end success
    error: function(error) {
       flashMessage('danger', 'Error: post not deleted');
    }// end error
  }); // end ajax 
}

$(document).on('click', '.readMore', function(event) {
  $postId = $(this).closest('.parentDiv').attr('id');
  location.href = "/read/" + $postId;
})

$(document).ready(function(){
  fetchPosts();
}); // end ready