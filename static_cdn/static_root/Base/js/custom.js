$(function () {

 



    $('.slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        speed: 1000,
        autoplaySpeed: 2000,
        nextArrow: '.right_arrow',
        prevArrow: '.left_arrow',
        dots: true
    });

    $('.text_slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        speed: 1000,
        autoplaySpeed: 2000,
        dots: false,
        arrows: false,
        fade: true,
        asNavFor: '.gallery_image'
    });
    $('.gallery_image').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        speed: 1000,
        autoplaySpeed: 2000,
        dots: false,
        nextArrow: '.photo_left',
        prevArrow: '.photo_right',
        asNavFor: '.text_slider'
    });

    /* tabs nav */
    $('#myTabs a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    //    back to top
    // Show or hide the sticky footer button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $('.go-top').fadeIn(200);
        } else {
            $('.go-top').fadeOut(200);
        }
    });
    // Animate the scroll to top
    $('.go-top').click(function (event) {
        event.preventDefault();

        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    })
 
});



















