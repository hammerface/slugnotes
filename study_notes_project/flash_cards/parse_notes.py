import re

# input: String of contents of file
# output: A list representing a deck of cards. Each element of the list is
#   itself a list. The first element of an inner list is the string on the
#   front of the card and the rest of the elements are strings of the bullet
#   points on the back of the card.
#   Returns an empty list in the case where there are no cards.
def parse_notes(data):
    deck = []
    front_found = False
    curr_card = None
    array = data.split('\n')
    for line in array:
        print line
        if front_found:
            match = re.search("^B:\s*(.*)$", line)
            if match:
                curr_card.append(match.group(1))
        match = re.search("^F:\s*(.*)$", line)
        if match:
            front_found = True
            curr_card = []
            curr_card.append(match.group(1))
            deck.append(curr_card)
    return deck

