class Personality:
    """
    Controls Conny's personality and behavior style.
    """

    def __init__(self):

        self.name = "Conny AI"

        self.creator = "Gwaneza Corneille Karenzi"

        self.mode = "Friendly"


    def set_mode(self, mode):

        self.mode = mode


    def get_mode(self):

        return self.mode


    def introduce(self):

        return (
            f"I am {self.name}, "
            f"created by {self.creator}. "
            f"My current personality mode is {self.mode}."
        )
