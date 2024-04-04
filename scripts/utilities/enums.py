from enum import Enum


class GameState(Enum):
    """
    Enumeration of possible game states.
    """
    MENU = 0
    GAME = 1
    DIALS = 2


# Enums below are to make it easy to add to the game in the future


class TileType(Enum):
    """
    Enumeration of Background Tiles
    """
    DEFAULT = 0


class EnemyName(Enum):
    """
    Enumeration of Enemy names
    """
    WEAK_PIN = 0
    STRONG_PIN = 1


class PlayerAttack(Enum):
    """
    Enumeration of Player Attacks
    """
    STRAIGHT_BALL = 0


class Pickups(Enum):
    """
    Enumeration of possible pickups
    """
    XP_SMALL = 0
    XP_BIG = 1


class PlayerUpgrades(Enum):
    """
    Enumeration of Player upgrades
    """
    SPEED = 0  # Speed upgrade
    HEALTH = 1  # Health upgrade
    ABSORB = 2  # Xp absorb upgrade


class SBUpgrades(Enum):
    """
    Enumeration of Straight Ball Upgrades
    """
    DAMAGE = 0  # Damage upgrade
    DURATION = 1  # SB Duration upgrade
    SPEED = 2  # SB Ball speed upgrade
    SECOND_BALL = 3  # SB Ball second ball upgrade


class UpgradeType:
    """
    Enumeration of upgrade value modification types.
    """
    MULTIPLICATION = 0
    ADDITION = 1
    SUBTRACTION = 2
    BOOL = 3
