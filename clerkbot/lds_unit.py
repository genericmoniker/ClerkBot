class LDSUnit:
    """Queries against data from an LDSSession."""

    # Dumb brute-force implementations for now...

    def __init__(self, unit_data):
        self.data = unit_data

    def get_individual_by_id(self, id_):
        directory = self.data['households']
        for household in directory:
            for individual in self._flatten_household(household):
                if individual['individualId'] == id_:
                    return individual
        return None

    def get_individuals_by_calling(self, calling_name):
        individuals = []
        for calling in self._flatten_callings(self.data['callings']):
            if calling['positionName'] == calling_name:
                individual = self.get_individual_by_id(calling['individualId'])
                individuals.append(individual)
        return individuals

    @staticmethod
    def _flatten_household(household):
        yield household['headOfHouse']
        if 'spouse' in household:
            yield household['spouse']
        if 'children' in household:
            yield from household['children']

    @staticmethod
    def _flatten_callings(callings: list):
        """Yield callings as a flat list.

        A calling is a dict with a positionName.
        """
        for item in callings:
            if isinstance(item, dict):
                if 'positionName' in item:
                    yield item
                elif 'children' in item:
                    yield from LDSUnit._flatten_callings(item['children'])
                elif 'assignmentsInGroup' in item:
                    yield from LDSUnit._flatten_callings(
                        item['assignmentsInGroup']
                    )
