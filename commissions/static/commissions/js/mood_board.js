$(document).ready(function(){
    $('.modal').modal();
    $(`input[type="file"]:gt(0)`).parent().addClass('hide');
    M.textareaAutoResize($('#id_description'));

    for (var i = 0; i < $('input[type="file"]').length; i++) {
        if ($(`input[type="file"]:eq(${i})`).siblings('a').length > 0 ) {
            var fileUrl = $(`input[type="file"]:eq(${i})`).siblings('a').attr('href');
            var filePath = fileUrl.split('/');
            var fileName = filePath[filePath.length - 1];

            $(`.mood-board-image:eq(${i}) > img`).attr('src', fileUrl);
            $(`.mood-board-image:eq(${i}) > p:first`).text(`File name: ${fileName}`);
            $(`.mood-board-image:eq(${i})`).removeClass('hide');
            $(`input[type="file"]:eq(${i})`).parent().addClass('hide');
            $(`input[type="file"]:eq(${i+1})`).parent().removeClass('hide');
        } else {
            $(`.mood-board-image:eq(${i})`).addClass('hide');
        }
    }

    $('input[type="file"]').change(function() {
        var fileCount = $('input[type="file"]').index(this);
        
        // Create URL for file preview found in https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
        var file = $(this)[0].files[0];
        var fileUrl = URL.createObjectURL(file);
        
        $(`input[type="file"]:eq(${fileCount})`).siblings($(`input[type="checkbox"]`)).attr(
            "checked", true);
        $(`.mood-board-image:eq(${fileCount}) > img`).attr('src', fileUrl);
        $(`.mood-board-image:eq(${fileCount}) > p:first`).text(`File name: ${file.name}`);
        $(`.mood-board-image:eq(${fileCount})`).removeClass('hide');

        $(this).parent().addClass('hide');
        for (var i = fileCount + 1; i < $('input[type="file"]').length; i++) {
            if ($(`.mood-board-image:eq(${i}) > img`).attr('src') === "#") {
                $(`input[type="file"]:eq(${i})`).parent().removeClass('hide');
                break
            }
        }
    });

    $('.mood-board-image .btn-flat').click(function() {
        var fileNumber = $('.mood-board-image .btn-flat').index(this);
        
        $(`input[type="file"]:eq(${fileNumber})`).val("");
        $(`input[type="file"]:eq(${fileNumber})`).siblings($(`input[type="checkbox"]`)).attr(
            "checked", true);
        $(`.mood-board-image:eq(${fileNumber}) > img`).attr('src', "#");
        $(`.mood-board-image:eq(${fileNumber}) > p:first`).text(`File name: `);
        $(`.mood-board-image:eq(${fileNumber})`).addClass('hide');

        $(`input[type="file"]:gt(${fileNumber})`).parent().addClass('hide');
        $(`input[type="file"]:eq(${fileNumber})`).parent().removeClass('hide');
    });
});

