"""An environment wrapper to convert binary to discrete action space."""
import gym
import numpy as np


class BinarySpaceToDiscreteSpaceEnv(gym.Wrapper):
    """An environment wrapper to convert binary to discrete action space."""

    # a mapping of buttons to binary values
    _button_map = {
        'right':  0b10000000,
        'left':   0b01000000,
        'down':   0b00100000,
        'up':     0b00010000,
        'start':  0b00001000,
        'select': 0b00000100,
        'B':      0b00000010,
        'A':      0b00000001,
        'NOP':    0b00000000,
    }

    def __init__(self, env, actions):
        """
        Initialize a new binary to discrete action space wrapper.

        Args:
            env (gym.Env): the environment to wrap
            actions (list): an ordered list of actions (as lists of buttons).
                The index of each button list is its discrete coded value

        Returns:
            None

        """
        super(BinarySpaceToDiscreteSpaceEnv, self).__init__(env)
        # create the new action space
        self.action_space = gym.spaces.Discrete(len(actions))
        # create the action map from the list of discrete actions
        self._action_map = {}
        # iterate over all the actions (as button lists)
        for action, button_list in enumerate(actions):
            # the value of this action's bitmap
            byte_action = 0
            # iterate over the buttons in this button list
            for button in button_list:
                byte_action |= self._button_map[button]
            # set this action maps value to the byte action value
            self._action_map[action] = byte_action

    def step(self, action):
        """
        Take a step using the given action.

        Args:
            action (int): the discrete action to perform

        Returns:
            a tuple of:
            - (numpy.ndarray) the state as a result of the action
            - (float) the reward achieved by taking the action
            - (bool) a flag denoting whether the episode has ended
            - (dict) a dictionary of extra information

        """
        # take the step and record the output
        return self.env.step(self._action_map[action])

    def reset(self):
        """Reset the environment and return the initial observation."""
        return self.env.reset()

# explicitly define the outward facing API of this module
__all__ = [BinarySpaceToDiscreteSpaceEnv.__name__]
