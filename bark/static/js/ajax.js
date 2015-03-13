/**
 * Created by Lewis on 13/03/2015.
 */

$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/bark/suggest_category/', {suggestion: query}, function(data){
         $('#tags').html(data);
        });
});
