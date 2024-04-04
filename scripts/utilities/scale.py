class Scale:
    """Class to scale the game's resolution."""
    def __init__(self):
        self.scale = False

    def r1440(self, num):
        """
        Rescale the game's image to 1440p resolution.
        :param num:
        :return:
        """
        if isinstance(num, int):
            return num*2

    def speed_scale(self, speed):
        """
        Scale an object's speed attribute.'
        :param speed:
        :return:
        """
        return int(speed)*2


# Allows all classes to access the scale class
scale_singleton = Scale()
