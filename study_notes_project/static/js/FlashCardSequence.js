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
    alert("flip");
    var card_content = $('.seq-in');
    console.log(card_content.find('.fcseq_card_front'));
    card_content.find('.fcseq_card_front').toggleClass('hidden');
    console.log(card_content.find('.fcseq_card_back'));
    card_content.find('.fcseq_card_back').toggleClass('hidden');
});