$(document).ready(function() {
    $('#branding').remove()
    if ($("#result-number").text().trim().length) {
        $(".result-area").show();
        $(".project-title").css("padding-top", "0px");
        $('center').contents().unwrap();
        $(".search-area").css("display", "inline-block");
        $(".search-area").css("position", "absolute");
        $(".search-area").css("margin", "-9px");
         $(".result-area").css("margin-top", "50px");
        $(".project-title").css("display", "inline-block");
        $(".site-subtitle").hide()
        $(".top-bar").css("background-color", "lavender")
    }
    if (!($("#result-number").text().trim().length)) {
        $(".result-area").hide();
    }
    var myDiv = $('.abstract-text');
    myDiv.text(myDiv.text().substring(0,300));
});