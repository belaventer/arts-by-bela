$(document).ready(function(){
    $('.collapsible').collapsible();
    if ($('#id_client_comment').length > 0){
       M.textareaAutoResize($('#id_client_comment')); 
    }
    

    $('input[type="file"]').change(function() {
        var file = $(this)[0].files[0];
        var fileUrl = URL.createObjectURL(file);

        $(this).prevAll('img').attr('src', fileUrl).removeClass('hide');
        $(this).prevAll('p').text(`File name: ${file.name}`);
        $(this).prevAll('button').removeClass('hide');
    });

});

