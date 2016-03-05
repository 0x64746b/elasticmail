jQuery(document).ready(function($) {
    $(".clickable-rows tr").click(function() {
        $(this).next().toggleClass('hidden')
    });
});

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 3000);
