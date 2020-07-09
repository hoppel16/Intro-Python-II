# Implement a class to hold room information. This should have name and
# description attributes.


class Room:
    def __init__(self, name, description,items=None):
        if items is None:
            items = []
        self.name = name
        self.description = description
        self.items = items

    def __str__(self):
        return "\033[95mLocation: {self.name}.\n{self.description}".format(self=self)
