
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//http://coreymaynard.com/blog/performing-ajax-post-requests-in-django/
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

//https://realpython.com/blog/python/django-and-ajax-form-submissions/
function addNewDeck() {
	$('#make-deck-submit').click(function(event){
		event.preventDefault();
		var user = $("#id_user").val();
		var deck_name = $("#id_deck_name").val();
		var share_flag = $('#id_share_flag').is(':checked');
		// var csrftoken = getCookie('csrftoken');

		//start ajax post
		$.ajax({
        url : "/cards/new_deck/", // the endpoint
        type : "POST", // http method
        data : { user : user, deck_name : deck_name, share_flag : share_flag }, // data sent with the post request
        "beforeSend": function(xhr, settings) {
        console.log("Before Send");
        $.ajaxSettings.beforeSend(xhr, settings);
    	},
        // handle a successful response
        success : function(json) {
            //http://stackoverflow.com/questions/2624761/returning-form-errors-for-ajax-request-in-django
            var errors = jQuery.parseJSON(json);

            //erros in form
            if (errors.deck_name != null) {
            	var error = $('#make-deck-error');
            	error.text(errors.deck_name)
            }else {
            	//no errors in form
            	$('#make-deck-form').trigger("reset");
            	var cancelButton = document.getElementById("make-deck-cancel");
				cancelButton.click();
				location.reload();
            }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
            //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
               // " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

		
		
	});
}




$(document).ready(function(){
	addNewDeck();
    $('h6.deck_name').each(function() {
        var text_length = $(this).width();
        var padding = (172-text_length)/2 + 36;
        $(this).css("left",padding)
    });

    $('div.deck').hover(
        function(){
            $(this).find('.image-caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.image-caption').slideUp(250); //.fadeOut(205)
        }
    );

    $('.image-caption a').tooltip();


});