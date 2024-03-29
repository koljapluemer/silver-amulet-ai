import gymnasium as gym
import gymnasium.spaces as spaces
import random
import numpy as np

class CardGameEnv(gym.Env):
    def __init__(self):
        super(CardGameEnv, self).__init__()

        # Define action and observation spaces
        # use only Box, Discrete, MultiBinary or MultiDiscrete spaces
    #    replace dict config:
        self.action_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(5)))
        self.observation_space = spaces.Dict({
            'player_hands': spaces.MultiDiscrete([13] * 4 * 5),
            'pile_top_card': spaces.Discrete(13),
            'current_player': spaces.Discrete(4),
        })

        # self.action_space = gym.spaces.Discrete(7)

        # Initialize game state
        self.reset()

    def reset(self):
        # Reset the game state to its initial configuration
        self.deck = list(range(52))
        random.shuffle(self.deck)
        
        player_hands = [[self.deck.pop() % 13 for _ in range(5)] for _ in range(4)]

        self.state = {
            'player_hands': player_hands,
            'pile_top_card': self.deck.pop() % 13,
            'current_player': 0,
        }
        return self.state

    def step(self, action):
        # Take an action (keep or discard the card) and update the game state accordingly
        player = self.state['current_player']
        keep_card, discard_index = action
        prev_hand_card_sum = sum(self.state['player_hands'][player])

        if keep_card:  # Keep
            self.state['player_hands'][player][discard_index] = self.state['pile_top_card']

        # Draw a new card from the deck if available
        if self.deck:
            self.state['pile_top_card'] = self.deck.pop() % 13
        else:
            self.state['pile_top_card'] = None

        self.state['current_player'] = (player + 1) % 4

        if not self.deck:
            # Calculate scores
            scores = [sum(hand) for hand in self.state['player_hands']]
            winner = scores.index(min(scores))
            # reward = 1 if player == winner else -1
            done = True
        else:
            # reward = 0
            done = False

        # calculate sum of hand cards
        current_hand_card_sum = sum(self.state['player_hands'][player])
        reward =  prev_hand_card_sum - current_hand_card_sum
        print("Player", player, "reward:", reward)

        info = {}  # Any additional information

        return self.state, reward, done, info

    def render(self, mode='human'):
        # Provide a human-readable representation of the game state
        print("Player hands:", self.state['player_hands'])
        print("Pile top card:", self.state['pile_top_card'])
        print("Current player:", self.state['current_player'])
