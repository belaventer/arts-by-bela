$(document).ready(function(){
    const sizeSelected = JSON.parse($('#commission-size').text());
    const resolutionSelected = JSON.parse($('#commission-resolution').text());
    var sizeList = $('.select-wrapper ul')[0];
    var resList = $('.select-wrapper ul')[1];
    var sizeOptions = $('#id_size_price');
    var resOptions = $('#id_resolution_price');
    var option;
    var selectOption;
    
    for (var i = 0; i < $(sizeList).children().length; i++) {
        option = $(sizeList).children()[i];
        selectOption = $(sizeOptions).children()[i];
        $(option).removeClass('selected');
        if ($(option).children().text() === sizeSelected) {
            $(selectOption).prop('selected', true);
            $(option).addClass('selected');
            $(sizeList).prev().val(sizeSelected);
        }
    }

    for (i = 0; i < $(resList).children().length; i++) {
        option = $(resList).children()[i];
        selectOption = $(resOptions).children()[i];
        $(option).removeClass('selected');
        if ($(option).children().text() === resolutionSelected) {
            $(selectOption).prop('selected', true);
            $(option).addClass('selected');
            $(resList).prev().val(resolutionSelected);
        }

        $('#your-quote').text(
            `$ ${calculateQuote(
                    getPriceFactor(
                        data.resolutions, 'resolution', $('.selected').children().last().text()),
                    getPriceFactor(
                        data.sizes, 'size', $('.selected').children().first().text()),
                    $('#id_number_characters').val())}`);
    }
});