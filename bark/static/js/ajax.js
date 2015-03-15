/**
 * Created by Lewis on 13/03/2015.
 */

$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/bark/suggest_tags/', {suggestion: query}, function(data){
         $('#tags').html(data);
        });
});

$('#rating').click(function(){
    var Post_slug;
    catid = $(this).attr("data-Post_slug");
    $.get('/bark/like_post/', {Post_slug: Post_slug}, function(data){
               $('#rating_count').html(data);
               $('#rating').hide();
    });
});