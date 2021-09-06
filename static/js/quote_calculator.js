// Script to dynamically calculate quote price from selected specifications.
const data = JSON.parse($('#json-data').text());
var res_price = 0.0;
var size_price = 0.0;

$(document).ready(function(){
    $('#lowest-price').text(
        `$ ${calculateQuote(
            data.resolutions[0].price_factor,data.sizes[0].price_factor,0)}!!`);
    $('#your-quote').text(
        `$ ${calculateQuote(
                getPriceFactor(
                    data.resolutions, 'resolution', $('.selected').children().last().text()),
                getPriceFactor(
                    data.sizes, 'size', $('.selected').children().first().text()),
                $('#id_number_characters').val())}`);
    $('#calculator-select').children().change(function (){
        res_price = getPriceFactor(
            data.resolutions, 'resolution', $('.selected').children().last().text());
        size_price = getPriceFactor(
            data.sizes, 'size', $('.selected').children().first().text());
        $('#your-quote').text(`$ ${calculateQuote(
            res_price,size_price,$('#id_number_characters').val())}`);
        }
    );
});

function calculateQuote(res, sizing, numberCharacters){
    return (5*res*sizing+2*numberCharacters).toFixed(2)
}

function getPriceFactor(array, key, selection) {
    // Function to get price factor from the JSON data
    for (item in array) {
        if (key === 'resolution') {
            if (array[item].resolution === selection) {
                return array[item].price_factor
            }
        } else {
            if (array[item].size === selection) {
                return array[item].price_factor
            }
        }
    }
}
