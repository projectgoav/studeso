/**
 * Created by paul on 17/03/15.
 */

$(document).ready(function(){
    new Taggle('tags', {
        placeholder: 'Press return to add tag...',
        duplicateTagClass: 'bounce',
        tabIndex: 1
    });
});
