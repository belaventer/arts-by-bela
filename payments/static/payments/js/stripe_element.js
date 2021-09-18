var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var commissionId = $('#commission_id').text();
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#9e9e9e',
        fontFamily: '"Montserrat", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#F44336',
        iconColor: '#F44336'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Display validation errors on the card element
card.addEventListener('change', function (event) {
  var errorDiv = document.getElementById('card-errors');
  if (event.error) {
      var html = `<span class="icon" role="alert">
          <i class="tiny material-icons">error</i>
          </span>
          <span>${event.error.message}</span>`;
      $(errorDiv).html(html);
  } else {
      errorDiv.textContent = '';
  }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({ 'disabled': true});
  $('#submit-button').attr('disabled', true);
  $('#loader').fadeIn();
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var postData = {
    'client_secret': clientSecret,
    'commission_id': commissionId,
    'csrfmiddlewaretoken': csrfToken
  };
  var url = '/payment/cache_commission/';

  $.post(url, postData).done(function(){
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
      },
    }).then(function(result) {
      if (result.error) {
        var errorDiv = document.getElementById('card-errors');
        var html = `<span class="icon" role="alert">
          <i class="tiny material-icons">error</i>
          </span>
          <span>${result.error.message}</span>`;
        $(errorDiv).html(html);
        $('#loader').fadeOut();
        card.update({ 'disabled': false});
        $('#submit-button').attr('disabled', false);
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          form.submit();
        }
      }
      });
  }).fail(function () {
    location.reload();
  });
});