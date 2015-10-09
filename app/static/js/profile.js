var appendUserPosts = function(posts) {
	$.each(posts, function(i, post){
		$item = '<li id="' + post.id +'" class="list-group-item">' +
				post.title +
				'<div class="pull-right"><span style="cursor:pointer" class="editPost pull-left glyphicon glyphicon-pencil">'+
				'</span>&nbsp;&nbsp;<span style="cursor:pointer" class="deletePost pull-right glyphicon glyphicon-remove">'+
				'</span></div></li>';
		$('#userPosts').append($item);
	})
}

var appendLikedPosts = function(posts) {
	$.each(posts, function(i, post){
		$item = '<li id="' + post.id +'" class="list-group-item">' +
				post.title +
				'<span style="cursor:pointer" class="likeStatus pull-right glyphicon glyphicon-remove">'+
				'</span></li>';
		$('#likedPosts').append($item);
	})
}

var appendUserInfo = function(info) {
	$registeredOn = moment( info.created ).format('YYYY-MM-DD');
	$('#username').text(info.username);
	$('#email').text(info.email);
	$('#registeredOn').text($registeredOn);
	$('#editUsername').attr('value', info.username);
	$('#editEmail').attr('value', info.email);
}

$(document).on('click', '.editPost', function(event){
	$postId = $( this ).closest('li').attr('id');
	location.href = "/edit/" + $postId;
})

$(document).on('click', '.deletePost', function(event){
	$confirmDelete = confirm('Delete post?');
	if ( $confirmDelete == false ) {
		return;
	}
	$post = $( this ).closest('li');
	$postId = $( this ).closest('li').attr('id');
	setToken();
	$.ajax({
		url: '/posts/' + $postId,
		type: 'DELETE',
		success: function(response) {
			flashMessage('success', 'Post deleted');
			$post.remove();
		},
		error: function(error) {
			flashMessage('danger', 'Post not deleted');
		}
	})
})

$(document).on('click', '.likeStatus', function(event){
	$post = $(this).parent();
	$postId = $(this).parent().attr('id');
	$confirmUnlike = confirm('Want to unlike post?');
	if ($confirmUnlike) {
		setToken();
		$.ajax({
			url: '/like',
			type: 'POST',
			data: {'post_id': $postId},
			success: function(data) {
				$post.remove();
				flashMessage('success', 'Post unliked')
			},
			error: function(error) {
				flashMessage('danger', 'Error: Status not changed');
			}
		})
	}
})

$(document).on('click', '.editInfoBtn', function(event){
	$('#email').toggle();
	$('#username').toggle();
	$('.editInfo').toggle();
})

var setToken = function() {
	csrftoken = $('meta[name=csrf-token]').attr('content');
	$.ajaxSetup({
	  beforeSend: function(xhr, settings) {
	      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	          xhr.setRequestHeader("X-CSRFToken", csrftoken)
	      }
	  }
	})
}

$(document).on('click', '#updateUserInfo', function(event) {
	$oldemail = $('#email').text();
	$newemail = $('#editEmail').val();
	$newname = $('#editUsername').val();
	setToken();
	$.ajax({
		url: '/user',
		type: 'PUT',
		data: {'oldemail': $oldemail,
			   'newname': $newname, 
			   'newemail': $newemail},
		success: function(data){
			flashMessage('success', 'Info updated');
			// update profile info
			$('#username').text($newname);
			$('#email').text($newemail);
			$('#editUsername').attr('value', $newname);
			$('#editEmail').attr('value', $newemail);
		},
		error: function(error){
			flashMessage('danger', 'Info failed to updated');
		}
	});// end ajax
})

var flashMessage = function(type, message) {
  $('.flashedMessage').remove()
  $flash_div = '<div class="flashedMessage col-md-offset-4 col-md-4 alert alert-'+ type +'">' +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +       
        message +
    '</div><div class="clearfix"></div>';
  $('#profileContainer').prepend($flash_div);
} // end flashMessage

$(document).ready(function(){
	$.ajax({
		url: '/user',
		type: 'GET',
		success: function(data) {
			appendUserPosts(data.user_posts);
			appendUserInfo(data.user_info);
			appendLikedPosts(data.liked_posts);
		},
		error: function(error) {
			console.log('Error: ', error)
		}
	})
})