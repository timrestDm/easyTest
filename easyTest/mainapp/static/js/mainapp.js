
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

$(function() {
    $('.hidden_answers_forms').hide();
});

$(function() {
    $('.more_answers p').click(function() {
        $('.hidden_answers_forms').toggle();
    });
});

$(function() {
    if($("#sortable1").length >= 1) {
        $( "#sortable1, #sortable2" ).sortable({
            connectWith: ".connectedSortable"
        }).disableSelection();
}
} );
$(document).ready(function(){
    $( "#sortable2" ).mouseover(function() {
        var numItems = $("#sortable2 .ui-state-highlight").length;
        console.log(numItems)
        if(numItems > 0) {
            $("#submit_b").removeAttr("disabled").removeClass("disabled"); // Не DRY ! строчка дублирует функционал input_answer() Вероятно нужно вынести в отдельную функцию   
    };
    } );  
} );  
    
$(function() {
    $('.question_create_form label[for="id_description"]').before("<p>либо создайте вопрос, внося данные <br>в поля ввода и выбирая параметры</p>");
});

$(function() {
    $('label[for="id_title"]').before("<p>либо создайте тест, внося данные <br>в поля ввода и выбирая параметры</p>");
});

$(function() {
    var height = $('#sortable1').height();
    $('#sortable1').height(height);
    $('#sortable2').height(height);
});