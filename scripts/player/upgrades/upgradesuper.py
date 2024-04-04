from scripts.utilities.enums import UpgradeType

class UpgradeSuper:
    """Customizable class for all upgrade types."""
    def __init__(self, value, tier, tier_max, modifier, mod_type):

        self.is_maxed = False
        self.value = value
        self.tier = tier
        self.tier_max = tier_max
        self.modifier = modifier
        self.mod_type = mod_type

    def apply_upgrade(self):
        """
        Applies data changes correctly no matter how the data should be modified.
        :return:
        """
        match self.mod_type:
            case UpgradeType.MULTIPLICATION:
                self.value *= self.modifier
            case UpgradeType.ADDITION:
                self.value += self.modifier
            case UpgradeType.SUBTRACTION:
                self.value -= self.modifier
            case UpgradeType.BOOL:
                self.value = not self.value
        self.tier += 1
        self.is_maxed = (self.tier >= self.tier_max)
