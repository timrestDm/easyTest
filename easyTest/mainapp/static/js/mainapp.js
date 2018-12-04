$(function() {
    var currenthref = window.location.href;
    var currenthref_part2 = currenthref.split('/')[3];
    var currenthref_part3 = currenthref.split('/')[4];

    if (currenthref_part2 == 'test') {
        if (currenthref_part3 == 'create'|| currenthref_part3 == 'edit') {
            toggle_test_forms();
            changeQuestions();
        } else {
        makeDisable();
        testFunction();
        sortable_on();
        sortable_height();
        sortable_move();
        passTimeToSession();
        }
    } else if (currenthref_part2 == 'question_create' || 'currenthref_part2 == question_edit') {
        toggle_q_type();
        toggle_answers_forms();
    }
});

function makeDisable() {
    $('#submit_b').addClass('disabled').attr('disabled','disabled');
};

function formattedNumber(number) {
    return ("0" + number).slice(-2)
}

function testFunction() {
    var [minutes, seconds] = $("#timer").text().split(":");
    var myVar = setInterval(myFunction, 1000);

    function myFunction() {
        if (minutes <= 0 && seconds <= 0) {
            clearInterval(myVar);
        } else if (minutes == 0 && seconds > 0) {
            seconds = seconds - 1;
        } else if (minutes > 0  && seconds == '00') {
            minutes = minutes - 1;
            seconds = 59;
        } else if (minutes > 0  && seconds > 0) {
            seconds = seconds - 1;
        };
        minutes = formattedNumber(minutes);
        seconds = formattedNumber(seconds);
        $("#timer").text(minutes + ":" + seconds);
    };
};

function passTimeToSession() {
    $(":submit").click(function () {
        $("#left_time").attr('value', $("#timer").text());
    });
};

function toggle_bt_NextSkip(button_on, button_off) {
    button_on.removeAttr('disabled').removeClass('disabled');
    button_off.addClass('disabled').attr('disabled','disabled');
};

function input_answer() {
    toggle_bt_NextSkip($('#submit_b'), $('#submit_skip'))
};

function toggle_answers_forms() {
    $('.hidden_answers_forms').hide();
    $('.more_answers p').click(function() {
        $('.hidden_answers_forms').toggle();
    });
};

function toggle_test_forms() {
    var form_input = $('.test_form_input')
    var form_json = $('.test_form_json')
    var bt_form_input = $('.create_input')
    var bt_form_json = $('.create_json')

    form_json.hide();
    bt_form_input.click(function() {
        form_input.show();
        form_json.hide();
        bt_form_input.addClass('tab_active');
        bt_form_json.removeClass('tab_active');
    });
    bt_form_json.click(function() {
        form_input.hide();
        form_json.show();
        bt_form_input.removeClass('tab_active');
        bt_form_json.addClass('tab_active');
    });
};

function sortable_on() {
    if($("#sortable1").length >= 1) {
        $( "#sortable1, #sortable2" ).sortable({
            connectWith: ".connectedSortable"
        }).disableSelection();
    }
};

function sortable_move() {
    $( ".answer_box").mouseover(function() {
        var numItems_1 = $("#sortable1 .ui-state-highlight").length;
        var numItems_2 = $("#sortable2 .ui-state-highlight").length;

        if(numItems_2 > 0 && numItems_1 == 0) {
            toggle_bt_NextSkip($('#submit_b'), $('#submit_skip'))
            $('input[name="skip_question"]').val('False');
        } else if (numItems_2 != 0 || numItems_1 != 0) {
            toggle_bt_NextSkip($('#submit_skip'), $('#submit_b'))
            $('input[name="skip_question"]').val('True');
        };
    });
};

function sortable_height() {
    var height = $('#sortable1').height();
    $('#sortable1').height(height);
    $('#sortable2').height(height);
};

function toggle_q_type() {
    var select_q_type = document.getElementById('id_q_type');
    select_q_type.setAttribute("onChange", "toggle_q_type(this)");

    var q_type = select_q_type.value
    var bl_is_correct = $('.answers_create input[type="checkbox"]').closest('li');
    var bl_order_num = $('.answers_create input[type="number"]').closest('li');

    if (q_type == 'select') {
        for (var i = 0; i < bl_order_num.length; i++) {
            bl_is_correct[i].style.display='flex';
            bl_order_num[i].style.display='none';
        }
    } else if (q_type == 'sort') {
        for (var i = 0; i < bl_order_num.length; i++) {
            bl_is_correct[i].style.display='none';
            bl_order_num[i].style.display='flex';
        }
    }
}

function changeQuestions() {
    $('#id_questions_filter').wrap("<div class='around_p'></div>");
    $('.around_p').append($('#change'));
};