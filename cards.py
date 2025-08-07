suits = {"hearts" : 0, "clubs": 1, "spades": 2, "diamonds": 3}
ranks = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9" : 9, "10": 10, "jack": 11, "queen": 12, "king" : 13, "ace": 14}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        if self.rank == 11:
            rank_str = "J"     
        elif self.rank == 12:
            rank_str = "Q"  
        elif self.rank == 13:
            rank_str = "K" 
        elif self.rank == 14:
            rank_str = "A"  
        else:
                rank_str = str(self.rank) 

        if self.suit == 0:
            suit_str = "H"     
        elif self.suit == 1:
            suit_str = "C"  
        elif self.suit == 2:
            suit_str = "S" 
        elif self.suit == 3:
            suit_str = "D" 


        return rank_str + suit_str
    
def create_deck():
    deck = []
    for suit in range(4):
        for rank in range(2, 15):
            deck.append(Card(rank, suit))
    return deck

if __name__ == "__main__":
    deck = create_deck()
    print(f"Deck has {len(deck)} cards")
    print(f"First 10 cards: {deck[:10]}")
    print(f"Last 5 cards: {deck[-5:]}")
    
    # Test specific cards
    ace_hearts = Card(14, 0)
    king_spades = Card(13, 2)
    two_clubs = Card(2, 1)
    
    print(f"Ace of hearts: {ace_hearts}")
    print(f"King of spades: {king_spades}")  
    print(f"Two of clubs: {two_clubs}")