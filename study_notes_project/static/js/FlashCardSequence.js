// Get the Sequence element
var sequenceElement = document.getElementById("sequence");

// Place your Sequence options here to override defaults
// See: http://sequencejs.com/documentation/#options
var options = {
    fadeStepWhenSkipped: false,
    reverseWhenNavigatingBackwards: true,
    nextButton: true,
    prevButton: true,
}

// if there is a sequence for the page
if(sequenceElement != null){
    // Launch Sequence on the element, and with the options we specified above
    var mySequence = sequence(sequenceElement, options);
}

$('div.fcseq_flip').click(function(){
    // toggle hidden class for headers
    var card_content = $('.seq-in');
    card_content.find('.fcseq_card_front').toggleClass('hidden');
    card_content.find('.fcseq_card_back').toggleClass('hidden');
    // toggle color class for div
    var containing_div = $('.seq')
    containing_div.toggleClass('fcseq_card_front');
    containing_div.toggleClass('fcseq_card_back');

    // scroll back to top
    $('#sequence').scrollTop(0);
    var new_card_content = $('.seq-in');
    // if scroll height is bigger than the div height, turn on scrolling
    if(new_card_content.outerHeight() < new_card_content[0].scrollHeight){
        $('#sequence').css("overflow-y", "auto");
    // otherwise, turn of scrolling
    } else {
        $('#sequence').css("overflow-y", "hidden");   
    }
});

$('div.fcseq_next').click(function(){
    var card_content = $('.seq-in');
    var numcards = $('ul.seq-canvas').attr('id');
    var currentcard = $('.seq-in').attr('id');
    var currentcardnum = currentcard.substring(4);
    // if current card is 1 and clicking next button, 
    // make previous button visible
    if(1==currentcardnum){
        $('a.seq-prev div').css('visibility', 'visible');
    }
    // if current card is second to last card and clicking next button, 
    // make next button hidden
    if(Number(numcards)-1==Number(currentcardnum)){
        $('a.seq-next div').css('visibility', 'hidden');
    }
    // after current card is animated off screen
    setTimeout(function(){
        var containing_div = $('.seq')
        // remove all front/back color classes
        containing_div.removeClass('fcseq_card_front fcseq_card_back');
        // add the front color class
        containing_div.addClass('fcseq_card_front');

        // remove hidden class from both front and back of the now "hidden" card 
        card_content.find('.fcseq_card_front, .fcseq_card_back').removeClass('hidden');
        // add hidden class to back of the card
        card_content.find('.fcseq_card_back').addClass('hidden');
    },400)

    // after new card begins to animate on screen
    setTimeout(function(){
        // scroll back to top
        $('#sequence').scrollTop(0);
        var new_card_content = $('.seq-in');
        // if scroll height is bigger than the div height, turn on scrolling
        if(new_card_content.outerHeight() < new_card_content[0].scrollHeight){
            $('#sequence').css("overflow-y", "auto");
        // otherwise, turn of scrolling
        } else {
            $('#sequence').css("overflow-y", "hidden");   
        }
    }, 500)

});

$('div.fcseq_prev').click(function(){
    var card_content = $('.seq-in');
    var numcards = $('ul.seq-canvas').attr('id');
    var currentcard = $('.seq-in').attr('id');
    var currentcardnum = currentcard.substring(4);
    // if current card is last and clicking previous button,
    // toggle no click on next
    if(numcards==currentcardnum){
        $("a.seq-next div").css('visibility', 'visible');
    }
    // if current card is 2 and clicking previous button,
    // toggle no click on prev
    if(2==currentcardnum){
        $('a.seq-prev div').css('visibility', 'hidden');
    }
    // after current card is animated off screen
    setTimeout(function(){
        var containing_div = $('.seq')
        // remove all front/back color classes
        containing_div.removeClass('fcseq_card_front fcseq_card_back');
        // add the front color class
        containing_div.addClass('fcseq_card_front');

        // remove hidden class from both front and back of the now "hidden" card 
        card_content.find('.fcseq_card_front, .fcseq_card_back').removeClass('hidden');
        // add hidden class to back of the card
        card_content.find('.fcseq_card_back').addClass('hidden');

    },400)

    // after new card begins to animate on screen
    setTimeout(function(){
        // scroll back to top
        $('#sequence').scrollTop(0);
        var new_card_content = $('.seq-in');
        // if scroll height is bigger than the div height, turn on scrolling
        if(new_card_content.outerHeight() < new_card_content[0].scrollHeight){
            $('#sequence').css("overflow-y", "auto");
        // otherwise, turn of scrolling
        } else {
            $('#sequence').css("overflow-y", "hidden");   
        }
    }, 500)
});

$('div.fcseq_random').click(function(){
    alert("randomize!");
    // grab all <li> elements
    // reorder them by changing their id's
});

