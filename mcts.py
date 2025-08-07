import math
import random
from cards import Card, create_deck
from hand_evaluator import hand_evaluator
from itertools import combinations

class MCTSNode:
    def __init__(self, known_cards, level, parent = None):
        self.known_cards = known_cards
        self.level = level
        self.parent = parent
        self.children = []

        self.visits = 0
        self.wins = 0

    def ucb1_value(self, c=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        if self.parent == None:
            return self.wins / self.visits
        
        exploitation = self.wins / self.visits
        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration
    
    def is_terminal(self):
        return self.level == 4
    
    def get_win_rate(self):
        if self.visits == 0:
            return 0
        return self.wins / self.visits


def get_available_cards(known_cards):
    all_cards = create_deck()
    available = []
    for card in all_cards:
        is_used = False
        for known_card in known_cards:
            if card.rank == known_card.rank and card.suit == known_card.suit:
                is_used = True
                break
        if not is_used:
            available.append(card)
    return available

def sample_cards(available_cards, num_cards, limit=1000):
    """Sample up to 1000 random combinations of num_cards"""
    if len(available_cards) < num_cards:
        return []
    
    # Get all possible combinations
    all_combos = list(combinations(available_cards, num_cards))
    
    # If too many combinations, randomly sample up to limit
    if len(all_combos) > limit:
        sampled_combos = random.sample(all_combos, limit)
    else:
        sampled_combos = all_combos
    
    # Convert tuples back to lists
    return [list(combo) for combo in sampled_combos]

def expand_node(node):
    if node.is_terminal():
        return None
    
    available = get_available_cards(node.known_cards)
    if node.level == 0:
        cards_needed = 2
    elif node.level == 1:
        cards_needed = 3
    elif node.level == 2:
        cards_needed = 1
    elif node.level == 3:  
        cards_needed = 1
    else:
        return None
    
    possible_combos = sample_cards(available, cards_needed, limit=1000)
    
    if not possible_combos:
        return None
    
    # Pick a random combination that hasn't been explored yet
    unexplored_combos = []
    for combo in possible_combos:
        # Check if this combo already exists as a child
        combo_exists = False
        for child in node.children:
            child_new_cards = child.known_cards[len(node.known_cards):]
            if len(child_new_cards) == len(combo):
                if all(c1.rank == c2.rank and c1.suit == c2.suit 
                       for c1, c2 in zip(sorted(child_new_cards, key=lambda x: (x.rank, x.suit)),
                                        sorted(combo, key=lambda x: (x.rank, x.suit)))):
                    combo_exists = True
                    break
        if not combo_exists:
            unexplored_combos.append(combo)
    
    if not unexplored_combos:
        return None  # All combinations already explored
    
    # Create new child with random unexplored combination
    new_cards = random.choice(unexplored_combos)
    child_known_cards = node.known_cards + new_cards
    child = MCTSNode(child_known_cards, node.level + 1, node)
    node.children.append(child)
    
    return child

def simulate_game(node, player_cards):
    """Complete random game and return 1 if player wins, 0 if loses"""
    # Get what cards we know so far
    current_cards = node.known_cards.copy()
    available = get_available_cards(current_cards)
    
    # Figure out what we still need based on level
    if node.level == 0:
        # Need opponent cards + full board (2 + 5 = 7 cards)
        needed_cards = random.sample(available, 7)
        opponent_cards = needed_cards[:2]
        board_cards = needed_cards[2:7]
    elif node.level == 1:
        # Have opponent cards, need board (5 cards)
        opponent_cards = current_cards[2:4]  # Opponent cards from tree
        board_cards = random.sample(available, 5)
    elif node.level == 2:
        # Have opponent + flop, need turn + river (2 cards)
        opponent_cards = current_cards[2:4]
        flop = current_cards[4:7]
        turn_river = random.sample(available, 2)
        board_cards = flop + turn_river
    elif node.level == 3:
        # Have opponent + flop + turn, need river (1 card)
        opponent_cards = current_cards[2:4]
        board = current_cards[4:8]
        river = random.sample(available, 1)
        board_cards = board + river
    else:  # level == 4
        # Everything known, just evaluate
        opponent_cards = current_cards[2:4]
        board_cards = current_cards[4:9]
    
    # Evaluate both hands (best 5 cards from 7)
    player_best = find_best_hand(player_cards + board_cards)
    opponent_best = find_best_hand(opponent_cards + board_cards)
    
    # DEBUG: Print first few simulations
    if random.random() < 0.01:  # Print 1% of simulations
        print(f"Player: {player_cards} + {board_cards[:3]}... = {player_best}")
        print(f"Opponent: {opponent_cards} + {board_cards[:3]}... = {opponent_best}")
        print(f"Player wins: {player_best > opponent_best}")
    
    # Compare hands
    if player_best > opponent_best:
        return 1
    elif player_best < opponent_best:
        return 0
    else:
        # Same hand type - need better tie-breaking
        # For now, let's call it a tie and give it to player 50% of time
        return 1 if random.random() < 0.5 else 0
    
def find_best_hand(seven_cards):
    """Find best 5-card hand from 7 cards"""
    best_hand_type = -1
    
    # Try all combinations of 5 cards from 7
    for combo in combinations(seven_cards, 5):
        hand_type = hand_evaluator(list(combo))
        if hand_type > best_hand_type:
            best_hand_type = hand_type
    
    return best_hand_type

def backpropagate(node, result):
    """Update win/visit counts up the tree"""
    current = node
    while current is not None:
        current.visits += 1
        current.wins += result
        current = current.parent

def select_node(root):
    """Select a leaf node using UCB1"""
    current = root
    
    # Keep going down until we hit a node that can be expanded
    while True:
        # If this node can be expanded (has unexplored children), return it
        if not current.is_terminal():
            available = get_available_cards(current.known_cards)
            if current.level == 0:
                cards_needed = 2
            elif current.level == 1:
                cards_needed = 3
            elif current.level == 2:
                cards_needed = 1
            elif current.level == 3:
                cards_needed = 1
            else:
                cards_needed = 0
            
            possible_combos = sample_cards(available, cards_needed, limit=1000) if cards_needed > 0 else []
            
            # Count unexplored combinations
            unexplored_count = 0
            for combo in possible_combos:
                combo_exists = False
                for child in current.children:
                    child_new_cards = child.known_cards[len(current.known_cards):]
                    if len(child_new_cards) == len(combo):
                        if all(c1.rank == c2.rank and c1.suit == c2.suit 
                               for c1, c2 in zip(sorted(child_new_cards, key=lambda x: (x.rank, x.suit)),
                                                sorted(combo, key=lambda x: (x.rank, x.suit)))):
                            combo_exists = True
                            break
                if not combo_exists:
                    unexplored_count += 1
            
            # If there are unexplored children, this is our expansion target
            if unexplored_count > 0:
                return current
        
        # If no children exist, this is a leaf
        if not current.children:
            return current
        
        # Otherwise, select best child and continue
        current = max(current.children, key=lambda child: child.ucb1_value())
    
    return current

def mcts_estimate(player_cards, num_simulations=1000):
    """Main MCTS algorithm"""
    print(f"Running MCTS for {player_cards} with {num_simulations} simulations...")
    
    root = MCTSNode(player_cards, 0)
    
    for i in range(num_simulations):
        # 1. Selection - find leaf node to expand
        leaf = select_node(root)  # Remove path
        
        # 2. Expansion - add new child if possible
        if not leaf.is_terminal():
            new_child = expand_node(leaf)
            if new_child:
                leaf = new_child
        
        # 3. Simulation - random rollout
        result = simulate_game(leaf, player_cards)
        
        # 4. Backpropagation - update statistics
        backpropagate(leaf, result)
        
        # Print progress
        if (i + 1) % 200 == 0:
            win_rate = root.get_win_rate()
            print(f"Simulation {i+1}: Win rate = {win_rate:.4f}")
    
    return root.get_win_rate()

if __name__ == "__main__":
    # Test with fewer simulations first
    pocket_aces = [Card(14, 0), Card(14, 1)]
    win_rate = mcts_estimate(pocket_aces, 200)  # Just 200 simulations
    print(f"Final win rate for {pocket_aces}: {win_rate:.4f}")
    
    weak_hand = [Card(7, 0), Card(2, 1)]
    win_rate = mcts_estimate(weak_hand, 200)
    print(f"Final win rate for {weak_hand}: {win_rate:.4f}")