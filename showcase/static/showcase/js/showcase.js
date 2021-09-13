$('.carousel.carousel-slider').carousel({
});

$( ".showcase-item" ).click( function() {
    var windowHeight = $( window ).height();
    var windowWidth = $( window ).width();
    var imageHeight = $( this ).children('img').height();
    var imageWidht = $( this ).children('img').width();
    var imagePosition = $( this ).offset();
    var scroll = $( window ).scrollTop();
    var left;
    var top;

    left = (windowWidth/2+150 - imageWidht*1.5/2) - imagePosition.left;
    top = (windowHeight/2 - imageHeight*1.5/2) - imagePosition.top + scroll;

    for (var i = 0; i < $( ".showcase-item" ).length; i++) {
      if ( i != $( ".showcase-item" ).index(this)){
        $( `.showcase-item:eq(${i})` ).css({
            "transform": `matrix(1, 0, 0, 1, 0, 0)`,
            "transform-origin": "0% 0%",
            "z-index": 0,
          });
          $( `.showcase-item:eq(${i})` ).children('blockquote').fadeOut();
      }
    }

    if ($(this).css("z-index") != 9999) {
      $( this ).css({
        "transform": `matrix(1.5, 0, 0, 1.5, ${left}, ${top})`,
        "transform-origin": "0% 0%",
        "z-index": 9999,
      });
      $(this).children('blockquote').fadeIn();
    } else {
      $( this ).css({
        "transform": `matrix(1, 0, 0, 1, 0, 0)`,
        "transform-origin": "0% 0%",
        "z-index": 0,
      });
      $(this).children('blockquote').fadeOut();
    }
});
