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
    // enable scrolling for flashcard if necessary
    setTimeout(set_scroll, 300)
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
    // enable scrolling for flashcard if necessary
    set_scroll();
});

$('div.fcseq_next').click(function(){
    var card_content = $('.seq-in');
    var numcards = mySequence.$steps.length;
    var currentcardnum = mySequence.currentStepId;
    // if current card is 1 and clicking next button, 
    // make previous button visible
    if(1 == currentcardnum){
        $('a.seq-prev div').css('visibility', 'visible');
        $('a.seq-prev').toggleClass('prevent-click');
    }
    // if current card is second to last card and clicking next button, 
    // make next button hidden
    if(numcards-1 == currentcardnum){
        $('a.seq-next div').css('visibility', 'hidden');
        $('a.seq-next').toggleClass('prevent-click');
    }
    // after current card is animated off screen
    setTimeout(function(){set_card_to_front(card_content)}, 400)
    // after new card begins to animate on screen
    setTimeout(set_scroll, 500)

});

$('div.fcseq_prev').click(function(){
    var card_content = $('.seq-in');
    var numcards = mySequence.$steps.length;
    var currentcardnum = mySequence.currentStepId;
    // if current card is last and clicking previous button,
    // toggle no click on next
    if(numcards == currentcardnum){
        $("a.seq-next div").css('visibility', 'visible');
        $('a.seq-next').toggleClass('prevent-click');
    }
    // if current card is 2 and clicking previous button,
    // toggle no click on prev
    if(2 == currentcardnum){
        $('a.seq-prev div').css('visibility', 'hidden');
        $('a.seq-prev').toggleClass('prevent-click');
    }
    // after current card is animated off screen
    setTimeout(function(){set_card_to_front(card_content)}, 400)
    // after new card begins to animate on screen
    setTimeout(set_scroll, 500)
});

$('div.fcseq_random').click(function(){
    // randomizing a "ul" in html was based off of 
    // http://stackoverflow.com/questions/7070054/javascript-shuffle-html-list-element-order
    var ul = document.querySelector("ul.seq-canvas"), // get the list
    random_ul = ul.cloneNode(true), // clone the list
    i = random_ul.children.length + 1;
    // shuffle the cloned list
    while( i-- > 0 )
        random_ul.appendChild( random_ul.children[Math.random() * i |0] );
    // copy shuffled list back to DOM element
    ul.parentNode.replaceChild(random_ul, ul);
    // reset card color/face
    set_card_to_front($('.seq-in'));
    // set previous button to be hidden and unclickable
    $('a.seq-prev div').css('visibility', 'hidden');
    $('a.seq-prev').removeClass('prevent-click');
    $('a.seq-prev').addClass('prevent-click');
    // set the next button to be visible and clickable
    $('a.seq-next div').css('visibility', 'visible');
    $('a.seq-next').removeClass('prevent-click');
    // destroy the current sequence and make a new one with the newly randomized cards
    mySequence.destroy();
    mySequence = sequence(sequenceElement, options);
    // enable scrolling for flashcard if necessary
    setTimeout(set_scroll, 300)

});

function set_scroll(){
        // scroll back to top
        $('#sequence').scrollTop(0);
        var new_card_content = $('.seq-in');
        // if content is too long to fit in the div, turn on scrolling
        if(new_card_content.outerHeight() < new_card_content[0].scrollHeight){
            $('#sequence').css("overflow-y", "auto");
        // otherwise, turn of scrolling
        } else {
            $('#sequence').css("overflow-y", "hidden");   
        }
}

function set_card_to_front(card_content){
        // set the color of the cards to the front-color
        var containing_div = $('.seq')
        containing_div.removeClass('fcseq_card_front fcseq_card_back');
        containing_div.addClass('fcseq_card_front');
        // set the now hidden card to display it's front
        card_content.find('.fcseq_card_front, .fcseq_card_back').removeClass('hidden');
        card_content.find('.fcseq_card_back').addClass('hidden');
}
