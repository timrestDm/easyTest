
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
        var numItems_1 = $("#sortable1 .ui-state-highlight").length;
        var numItems_2 = $("#sortable2 .ui-state-highlight").length;
        console.log(numItems_2)
        if(numItems_2 > 0 && numItems_1 == 0) {
            $("#submit_b").removeAttr("disabled").removeClass("disabled"); // Не DRY ! строчка дублирует функционал input_answer() Вероятно нужно вынести в отдельную функцию
            $('#submit_skip').addClass('disabled').attr('disabled','disabled');
            $('input[name="skip_question"]').val('False');
        } else {
            $("#submit_b").addClass('disabled').attr('disabled','disabled'); // Не DRY ! строчка дублирует функционал input_answer() Вероятно нужно вынести в отдельную функцию
            $('#submit_skip').removeAttr("disabled").removeClass("disabled");
            $('input[name="skip_question"]').val('True');
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

$(function() {
    var bl_order_num = $('.answers_create input[type="number"]').closest('li');

    document.getElementById('id_q_type').setAttribute("onChange", "Selected(this)");
    for (var i = 0; i < bl_order_num.length; i++) {
                bl_order_num[i].style.display='none';
            }
});

function Selected(target) {
        var label = target.value;
        var bl_is_correct = $('.answers_create input[type="checkbox"]').closest('li');
        var bl_order_num = $('.answers_create input[type="number"]').closest('li');

        if (label == 'select') {
            for (var i = 0; i < bl_is_correct.length; i++) {
                bl_is_correct[i].style.display='flex';
                bl_order_num[i].style.display='none';
            }
        } else if (label == 'sort') {
            for (var i = 0; i < bl_is_correct.length; i++) {
                bl_is_correct[i].style.display='none';
                bl_order_num[i].style.display='flex';
            }
        }

}