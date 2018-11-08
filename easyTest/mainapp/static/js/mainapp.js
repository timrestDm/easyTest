
$(function makeDisable() {
    $('#submit_b').addClass('disabled').attr('disabled','disabled');
});

$(function testFunction() {
    var [minutes, seconds] = $("#timer").text().split(":");
    var myVar = setInterval(myFunction, 1000);
    
    function myFunction() {
        if (minutes <= 0 && seconds <= 0) {
            clearInterval(myVar);
        } else if (minutes == 0 && seconds > 0) {
            seconds = seconds - 1;
            $("#timer").text(minutes + ":" + seconds);
        } else if (minutes > 0  && seconds == '00') {
            minutes = minutes - 1;
            seconds = 59;
            $("#timer").text(minutes + ":" + seconds);
        } else if (minutes > 0  && seconds > 0) {
            seconds = seconds - 1;
            $("#timer").text(minutes + ":" + seconds);
        };
    };
});

$(function passTimeToSession() {
    $(":submit").click(function () {
        $("#left_time").attr('value', $("#timer").text());
    });
});

function input_answer() {
    $('#submit_b').removeAttr('disabled').removeClass('disabled');
    $('#submit_skip').addClass('disabled').attr('disabled','disabled');
};


    
