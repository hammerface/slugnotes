
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
		alert($('#make-deck-form').serialize());
		form = $('#make-deck-form').serialize()
		// var user = $("#id_user").val();
		// var deck_name = $("#id_deck_name").val();
		// var share_flag = $('#id_share_flag').is(':checked');
		// var csrftoken = getCookie('csrftoken');

		//start ajax post
		$.ajax({
        url : "/cards/new_deck/", // the endpoint
        type : "POST", // http method
        data : { form : form}, // data sent with the post request
     //    "beforeSend": function(xhr, settings) {
     //    console.log("Before Send");
     //    $.ajaxSettings.beforeSend(xhr, settings);
    	// },
        // handle a successful response
        success : function(json) {
            // $('#post-text').val(''); // remove the value from the input
            // console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
            //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
               // " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

		//alert(user + deck_name + share_flag);
		var cancelButton = document.getElementById("make-deck-cancel");
		cancelButton.click();
		
	});
}




$(document).ready(function(){
	addNewDeck();
});