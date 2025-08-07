from cards import Card

def count_ranks(cards): 
    count = {}
    for card in cards:
        if card.rank in count:
            count[card.rank] += 1
        else:
            count[card.rank] = 1
    return count

def check_flush(cards):
    first_card = cards[0].suit
    for card in cards:
        if first_card != card.suit:
            return False
    return True

def check_straight(cards):
    ranks = [card.rank for card in cards]
    ranks.sort()
    for i in range(1, len(ranks)):
        if ranks[i] != ranks[i-1] + 1:
            return False
    return True

def hand_evaluator(cards):
    counts = count_ranks(cards)
    count_val = sorted(counts.values(), reverse=True)

    is_flush = check_flush(cards)
    is_straight = check_straight(cards)

    if is_flush and is_straight:
        return 8
    elif count_val == [4,1]: #4 of a kind
        return 7
    elif count_val == [3,2]: #full house - 3 of a kind + 2 pair
        return 6
    elif is_flush:
        return 5
    elif is_straight:
        return 4
    elif count_val == [3, 1, 1]: #3 of a kind
        return 3
    elif count_val == [2, 2, 1]: #2 pair
        return 2
    elif count_val == [2, 1, 1, 1]: # 1 pair
        return 1
    else:
        return 0


if __name__ == "__main__":
    # Test with pair of aces (not a flush)
    test_cards = [Card(14, 0), Card(14, 1), Card(10, 2), Card(8, 3), Card(6, 0)]
    result = count_ranks(test_cards)
    print(f"Cards: {test_cards}")
    print(f"Rank counts: {result}")
    print(f"Is flush: {check_flush(test_cards)}")
    print(f"Hand type: {hand_evaluator(test_cards)}")  # Should be 1 (pair)
    print()
    
    # Test with a flush (all hearts)
    flush_cards = [Card(14, 0), Card(10, 0), Card(8, 0), Card(6, 0), Card(4, 0)]
    print(f"Flush cards: {flush_cards}")
    print(f"Is flush: {check_flush(flush_cards)}")
    print(f"Hand type: {hand_evaluator(flush_cards)}")  # Should be 5 (flush)
    print()

    straight_cards = [Card(5, 0), Card(6, 1), Card(7, 2), Card(8, 3), Card(9, 0)]
    print(f"Straight cards: {straight_cards}")
    print(f"Is flush: {check_flush(straight_cards)}")
    print(f"Is straight: {check_straight(straight_cards)}")
    print(f"Hand type: {hand_evaluator(straight_cards)}")  # Should be 4 (straight)
    print()
    
    # Test four of a kind
    quads = [Card(8, 0), Card(8, 1), Card(8, 2), Card(8, 3), Card(3, 0)]
    print(f"Quads: {quads}")
    print(f"Hand type: {hand_evaluator(quads)}")  # Should be 7 (four of a kind)

