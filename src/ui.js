var slides=["splash","ker","started"];
var t_anchor=[1.5, 3.5, 5];
var c=0; // c <-> currentSlide

function goToSlide(t){
    if(t<0)t=0;
    if(t>2)t=2;
    goTo(t_anchor[t]);
    $('html,body').animate({scrollTop:$("#"+slides[t]).offset().top}, 1500);
}

$(".nav-box").click(function(){
    var ref=slides.indexOf($(this).attr('id').split("-")[0]);
    goToSlide(ref);
})

$('body').on('mousewheel', function(event) {
    var h= $(window).scrollTop();
    var wh= $(window).height();
    var t= 1.5+1.6*(h/wh);
    if(t<5) goTo(1.5+1.6*(h/wh));
});
