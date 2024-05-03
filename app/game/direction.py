class Direction:
    """
    This class represents directions between locations (Location class).

    :param name: Name of the direction. Represents bot phrase
        before go by this direction.
    :param location_id: Identifier of direction in database.
        Unique value among all Direction instances.
    :param location_level: Level that player should attain to
        unlock this direction.
    """

    def __init__(self, name: str, location_id: int, location_level: int):
        """
        Constructor method.
        """
        
        self.name: str = name
        self.location_id: int = location_id
        self.location_level: int = location_level
