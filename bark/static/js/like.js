/**
 * Created by paul on 18/03/15.
 */

var getPost = function(){
    var url = window.location.pathname;
    var pathArray = url.split('/');
    var postID = pathArray[2];

    return parseInt(postID);
};

$(document).ready(function(){
    var postID = getPost();
    var csrf_token = $.cookie('csrftoken');

    $('.like-post-btn').click(function(){
        $.ajax({
            type:"POST",
            url:"/like_post/",
            data: {post_id: postID, csrfmiddlewaretoken:csrf_token},
            success: function(data){
                console.log(data);
                $('.post-like-num').html(data);
                $('.like-post-btn').children().removeClass('glyphicon-thumbs-up').addClass('glyphicon-ok');

            },
            error: function(data){
                alert("Like adding failed, try again");
            }
        });
    });

    $('.comment-like').click(function(){
            var commentNum = parseInt(this.className.split(' ')[1].split('-')[2]);
            var button = this;

            $.ajax({
                type:"POST",
                url:"/like_comment/",
                data: {post_id: postID, comment_num:commentNum, csrfmiddlewaretoken:csrf_token},
                success: function(data){
                    $('.comment-like-counter-' + commentNum).html(data);
                    $(button).children().removeClass('glyphicon-thumbs-up').addClass('glyphicon-ok');
                },
                error: function(data){
                    alert("Like adding failed, try again");
                }
            });
        }

    );
});
