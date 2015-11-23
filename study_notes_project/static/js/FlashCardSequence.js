// Get the Sequence element
var sequenceElement = document.getElementById("sequence");

// Place your Sequence options here to override defaults
// See: http://sequencejs.com/documentation/#options
var options = {
	keyNavigation: true,
    fadeStepWhenSkipped: false,
    reverseWhenNavigatingBackwards: true,
    nextButton: true,
    prevButton: true,
}

// Launch Sequence on the element, and with the options we specified above
var mySequence = sequence(sequenceElement, options);



$('div.fcseq_flip').click(function(){
    // toggle hidden class for headers
    var card_content = $('.seq-in');
    card_content.find('.fcseq_card_front').toggleClass('hidden');
    card_content.find('.fcseq_card_back').toggleClass('hidden');
    // toggle color class for div
    var containing_div = $('.seq-screen')
    containing_div.toggleClass('fcseq_card_front');
    containing_div.toggleClass('fcseq_card_back');
});

$('div.fcseq_next, div.fcseq_prev').click(function(){
    alert("clicl");
    // toggle color class for div
    var containing_div = $('.seq-screen')
    containing_div.removeClass('fcseq_card_front fcseq_card_back');
    containing_div.addClass('fcseq_card_front');
});