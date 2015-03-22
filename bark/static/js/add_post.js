/**
 * Created by paul on 17/03/15.
 */

$(document).ready(function(){
    var taggle = new Taggle('tags', {
	tags: defaultTagList,
        placeholder: 'Press return to add tag...',
        duplicateTagClass: 'bounce',
        tabIndex: 5,

        onTagAdd: function(event, tag){
            if(tag.length > 30){
                taggle.remove(tag);
            }
        }
    });
});
