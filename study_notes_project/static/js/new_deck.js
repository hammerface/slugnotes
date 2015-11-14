
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

/**
 * Set the deck_id as a hidden field for the edit deck (deck settings) form
 * then set the deck name and share flag for the edit deck form
 */
function fillEditDeckForm(){
    $('.edit-deck-toggle').click(function(){
        var deck_id = $(this).parent().parent().attr('id');
        $('input[name=edit-deck-id]').val(deck_id);

        var deck_name = $(this).parent().siblings('.deck_name').text();
        var share_set = $(this).parent().siblings('.share-set').val();

        $('#id_deck_name_edit').val(deck_name);
        if (share_set == "no") {
            $('#id_share_flag_edit').prop('checked', false);
        }else if (share_set == "yes") {
            $('#id_share_flag_edit').prop('checked', true);
        }

    });
}
function fillDeleteDeckForm(){
    $('.toggle-delete-deck').click(function(){
	   var deck_id = $(this).parent().parent().attr('id');
        $('input[name=id-deck-id]').val(deck_id);
        deck_name = $(this).parent().siblings('.deck_name').text()
        $('#delete-deck-name-span').text(deck_name)
    });
}

/**
 * When edit card button is clicked fill in the edit form with the 
 * front and back of card text. Also fill in the id of the card 
 * to the hidden form field.
 */
function fillEditCardForm() {
    

    $('.edit-card').click(function(){
        var front_card = $(this).parent().siblings('.small_card_content').children('.card_front').text();
        var back_card = $(this).parent().siblings('.small_card_content').children('.card_back').html();
        back_card = back_card.replace(/<br\s*[\/]?>/gi, "\n");
        
        $('#id_card_front_edit').val(front_card);
        $('#id_card_back_edit').val(back_card);


    });

    $('.get-card-id').click(function(){
	var card_id = $(this).parent().parent().attr('id');
        $('input[name=id-card-id]').val(card_id);
    });
}

//https://realpython.com/blog/python/django-and-ajax-form-submissions/
function addNewDeck() {
	$('#make-deck-submit').click(function(event){
		event.preventDefault();
        $("#make-deck-submit").disabled = true;
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
                $("#make-deck-submit").disabled = false;
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

function cloneDeck() {
    $('.clone-deck-toggle').click(function(){
        var orig_deck_id = $(this).parent().parent().attr('id');
        $('input[name=clone-deck-id]').val(orig_deck_id);

    });



    $('#clone-deck-submit').click(function(event){
        event.preventDefault();
        $("#clone-deck-submit").disabled = true;
        var user = $("#user-id").val();
        var deck_name = $("#id_deck_name").val();
        var share_flag = $('#id_share_flag').is(':checked');
        var clone_deck_id = $('#clone-deck-id-input').val()
        // var csrftoken = getCookie('csrftoken');
        //start ajax post
        $.ajax({
        url : "/cards/clone/", // the endpoint
        type : "POST", // http method
        data : { user : user, deck_name : deck_name, share_flag : share_flag, clone_deck_id : clone_deck_id }, // data sent with the post request
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
                var error = $('#clone-deck-error');
                error.text(errors.deck_name)
                $("#clone-deck-submit").disabled = false;
            }else {
                //no errors in form
                $('#clone-deck-form').trigger("reset");
                var cancelButton = document.getElementById("clone-deck-cancel");
                cancelButton.click();
                //location.reload();
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

function editDeck() {
	$('#edit-deck-submit').click(function(event){
		event.preventDefault();
	    var user = $("#id_user").val();
	    var deck_id = $("input[name=edit-deck-id]").val();
		var deck_name = $("#id_deck_name_edit").val();
		var share_flag = $('#id_share_flag_edit').is(':checked');
		// var csrftoken = getCookie('csrftoken');
        
		//start ajax post
		$.ajax({
        url : "/cards/edit_deck/", // the endpoint
        type : "POST", // http method
        data : { user : user, deck_id : deck_id, deck_name : deck_name, share_flag : share_flag }, // data sent with the post request
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
            	var error = $('#edit-deck-error');
            	error.text(errors.deck_name)
            }else {
            	//no errors in form
            	$('#edit-deck-form').trigger("reset");
            	var cancelButton = document.getElementById("edit-deck-cancel");
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

function deleteDeck() {



    $('#delete-deck-submit').click(function(event){
	event.preventDefault();
	var deck = $("input[name=id-deck-id]").val();
        
	//start ajax post
	$.ajax({
            url : "/cards/delete_deck/", // the endpoint
            type : "POST", // http method
            data : { deck : deck }, // data sent with the post request
            "beforeSend": function(xhr, settings) {
		console.log("Before Send");
		$.ajaxSettings.beforeSend(xhr, settings);
    	    },
            // handle a successful response
            success : function(json) {
            	$('#delete-deck-form').trigger("reset");
            	var cancelButton = document.getElementById("delete-deck-cancel");
		cancelButton.click();
		location.reload();
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
		console.log("error");
            }
	});
		
    });
}

function addNewCard() {
    $('#make-card-submit').click(function(event){
        event.preventDefault();
        var deck = $("#id_deck").val();
        var front = $("#id_front").val();
        var back = $('#id_back').val();
        // var csrftoken = getCookie('csrftoken');
        //start ajax post
        $.ajax({
        url : "/cards/new_card/", // the endpoint
        type : "POST", // http method
        data : { deck : deck, front : front, back : back }, // data sent with the post request
        "beforeSend": function(xhr, settings) {
        console.log("Before Send");
        $.ajaxSettings.beforeSend(xhr, settings);
        },
        // handle a successful response
        success : function(json) {
            //http://stackoverflow.com/questions/2624761/returning-form-errors-for-ajax-request-in-django
            var errors = jQuery.parseJSON(json);
            //errors in form
            if (errors.front != null) {
                var error = $('#make-card-error');
                error.text(errors.front)
            }else {
                //no errors in form
                console.log("Trying to submit.");
                $('#make-card-form').trigger("reset");
                var cancelButton = document.getElementById("make-card-cancel");
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

function editCard() {
    $('#edit-card-submit').click(function(event){
	event.preventDefault();
	var card = $("input[name=id-card-id]").val();
	var deck = $("#id_deck").val();
    var front = $("#id_card_front_edit").val();
    var back = $('#id_card_back_edit').val();
	// var csrftoken = getCookie('csrftoken');
        
	//start ajax post
	$.ajax({
            url : "/cards/edit_card/", // the endpoint
            type : "POST", // http method
            data : { card : card, deck : deck, front : front, back : back }, // data sent with the post request
            "beforeSend": function(xhr, settings) {
		console.log("Before Send");
		$.ajaxSettings.beforeSend(xhr, settings);
    	    },
            // handle a successful response
            success : function(json) {
		//http://stackoverflow.com/questions/2624761/returning-form-errors-for-ajax-request-in-django
		var errors = jQuery.parseJSON(json);
		
		//erros in form
		if (errors.front != null) {
            	    var error = $('#edit-card-error');
            	    error.text(errors.front)
		}else {
            	    //no errors in form
            	    $('#edit-card-form').trigger("reset");
            	    var cancelButton = document.getElementById("edit-card-cancel");
		    cancelButton.click();
		    location.reload();
		}
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
		console.log("error");
            }
	});
		
    });
}

function deleteCard() {
    $('#delete-card-submit').click(function(event){
	event.preventDefault();
	var card = $("input[name=id-card-id]").val();
	var deck = $("#id_deck").val();
        
	//start ajax post
	$.ajax({
            url : "/cards/delete_card/", // the endpoint
            type : "POST", // http method
            data : { card : card, deck : deck }, // data sent with the post request
            "beforeSend": function(xhr, settings) {
		console.log("Before Send");
		$.ajaxSettings.beforeSend(xhr, settings);
    	    },
            // handle a successful response
            success : function(json) {
            	$('#delete-card-form').trigger("reset");
            	var cancelButton = document.getElementById("delete-card-cancel");
		cancelButton.click();
		location.reload();
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
		console.log("error");
            }
	});
		
    });
}

//centers deck name
function centerDeckName() {
    $('h6.deck_name').each(function() {
        var text_length = $(this).width();
        var padding = (172-text_length)/2 + 36;
        $(this).css("left",padding)
    });
}


//does a lot: text is too big for card it adds a scroll, if it fits it centers (cards)
function scrollText(){
    $('div.small_card_content').each(function(){
        if ($(this)[0].scrollHeight == $(this)[0].clientHeight){
            console.log("heights are equal");
            $(this).css("display","table-cell"); 
            $(this).addClass("link_here");
        } else {
            console.log("heights are not equal");      
            $(this).siblings('.image-caption').width(185);
            $(this).children('p').addClass("link_here")

        }
    });
}

//drop down deck
function deckDropDown(){
    $('div.deck').hover(
        function(){
            $(this).find('.image-caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.image-caption').slideUp(250); //.fadeOut(205)
        }
    );
}

//drop down user result
function userResultDropDown(){
    $('div.UserResult').hover(
        function(){
            $(this).find('.image-caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.image-caption').slideUp(250); //.fadeOut(205)
        }
    );
}

//drop down user result
function deckResultDropDown(){
    $('div.DeckResult').hover(
        function(){
            $(this).find('.image-caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.image-caption').slideUp(250); //.fadeOut(205)
        }
    );
}

//drop down cards
function cardsDropDown(){
    $('div.small_card').hover(
        function(){
            $(this).find('.image-caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.image-caption').slideUp(250); //.fadeOut(205)
        }
    );
}

//show tool tips
function showToolTips(){
    //on decks/cards
    $('.image-caption a').tooltip();

    //on create/upload
    $('div.icon-wrap').tooltip(); 
}

function handleCardTurn(){
    $('a.flip_card').click(function(){
        var small_card_content = $(this).parent().siblings(".small_card_content")
        console.log(small_card_content.children('p'));
        small_card_content.children('p').toggleClass('hidden');
        small_card_content.parent().toggleClass('back_of_card');
        console.log(small_card_content.children('p'));
        small_card_content.css("display","inline-block");
        if (small_card_content[0].scrollHeight == small_card_content[0].clientHeight){
            console.log("heights are equal");
            small_card_content.css("display","table-cell"); 
            small_card_content.siblings('.image-caption').width(200);
            small_card_content.siblings('.image-caption').slideUp(250);
        } else {
            console.log("heights are not equal");  
            small_card_content.css("display","inline-block");  
            small_card_content.css("overflow-y","auto");  
            small_card_content.siblings('.image-caption').width(185);
            small_card_content.siblings('.image-caption').slideUp(250);
        }
    });
}

function getSharedProfile() {
    $('button[name=shared-profile-button]').click(function(event){
	//event.preventDefault();
	var u_name = $(this).parent().parent().attr('id');
	var u_id = $(this).attr('id');
	var csrftoken = getCookie('csrftoken');
	
	//start ajax post
	$.ajax({
            url : "/cards/shared_decks/", // the endpoint
            type : "POST", // http method
            data : { u_id : u_id, u_name : u_name , csrftoken : csrftoken }, // data sent with the post request
            "beforeSend": function(xhr, settings) {
		$.ajaxSettings.beforeSend(xhr, settings);
    	    },
	    success : function(json) {
		location.replase(json);
            }
	});
    });
}

$(document).ready(function(){
    addNewDeck();
    editDeck();
    deleteDeck();
    addNewCard();
    editCard();
    deleteCard();
    centerDeckName();
    scrollText();
    deckDropDown();
    cardsDropDown();
    userResultDropDown();
    deckResultDropDown();
    showToolTips();
    handleCardTurn();
    fillEditDeckForm();
    fillDeleteDeckForm();
    fillEditCardForm();
    cloneDeck();
    getSharedProfile();

    // $(document.body).on({
    //     mouseenter: function() {
    //         $(this).siblings('.image-caption').slideDown(250);
    //     },
    //     mouseleave: function() {
    //         $(this).siblings('.image-caption').slideUp(250);
    //     }
    // }, '.link_here');


    


});
