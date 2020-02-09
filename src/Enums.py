from enum import Enum


class Team(Enum):
	RED = 0
	BLUE = 1


class Direction(Enum):
	LEFT = 0
	RIGHT = 1


class GameState(Enum):
	WF_PLAYER_ACTION = 0
	WF_WEAPON_ACTION_END = 1
	WF_ROUND_END = 2
