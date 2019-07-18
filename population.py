"""
Modelling Population Data

=== Module Description ===
This module contains a new class, PopulationTree, which is used to model
population data drawn from the World Bank API.
Even though this data has a fixed hierarchichal structure (only three levels:
world, region, and country), because we are able to model it using an
AbstractTree subclass, we can then run it through our treemap visualisation
tool to get a nice interactive graphical representation of this data.

NOTE: You'll need an Internet connection to access the World Bank API

Finished by James Park
"""
import json
import urllib.request as request

from tree_data import AbstractTree


# Constants for the World Bank API urls.
WORLD_BANK_BASE = 'http://api.worldbank.org/countries'
WORLD_BANK_POPULATIONS = (
    WORLD_BANK_BASE +
    '/all/indicators/SP.POP.TOTL?format=json&date=2014:2014&per_page=270'
)
WORLD_BANK_REGIONS = (
    WORLD_BANK_BASE + '?format=json&date=2014:2014&per_page=310'
)


class PopulationTree(AbstractTree):
    """A tree representation of country population data.

    This tree always has three levels:
      - The root represents the entire world.
      - Each node in the second level is a region (defined by the World Bank).
      - Each node in the third level is a country.

    The data_size attribute corresponds to the 2014 population of the country,
    as reported by the World Bank.

    See https://datahelpdesk.worldbank.org/ for details about this API.
    """
    def __init__(self, world, root=None, subtrees=None, data_size=0):
        """Initialize a new PopulationTree.

        If <world> is True, then this tree is the root of the population tree,
        and it should load data from the World Bank API.
        In this case, none of the other parameters are used.

        If <world> is False, pass the other arguments directly to the superclass
        constructor. Do NOT load new data from the World Bank API.

        @type self: PopulationTree
        @type world: bool
        @type root: object
        @type subtrees: list[PopulationTree] | None
        @type data_size: int

        >>> pt = PopulationTree(True)
        >>> pt._root
        'World'
        >>> pt.data_size
        7232277834
        >>> len(pt._subtrees)
        7
        >>> pt = PopulationTree(False)
        >>> pt._root is None
        True
        >>> len(pt._subtrees)
        0
        """
        if world:
            region_trees = _load_data()
            AbstractTree.__init__(self, 'World', region_trees)
        else:
            if subtrees is None:
                subtrees = []
            AbstractTree.__init__(self, root, subtrees, data_size)

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        @type self: PopulationTree
        @rtype: str
        """
        route = ''
        if self._parent_tree is None:
            return str(self._root)
        else:
            route += self._parent_tree.get_separator()
            route += ("\\" + str(self._root))  # seperates each node
        return route


def _load_data():
    """Create a list of trees corresponding to different world regions.

    Each tree consists of a root node -- the region -- attached to one or
    more leaves -- the countries in that region.

    @rtype: list[PopulationTree]

    >>> region_data = _load_data()
    >>> len(region_data)
    7
    >>> isinstance(region_data[0], PopulationTree)
    True
    >>> region_data[0].data_size in range(0, 7232277834)
    True
    """
    # Get data from World Bank API.
    country_populations = _get_population_data()
    regions = _get_region_data()
    rl = []
    for region in regions:
        p_l = []
        for country in country_populations:
            if country in regions[region]:
                pt = PopulationTree(False, country.strip(),
                                    [], country_populations[country])
                p_l += [pt]
        rt = PopulationTree(False, region.strip(), p_l)
        rl += [rt]
    return rl


def _get_population_data():
    """Return country population data from the World Bank.

    The return value is a dictionary, where the keys are country names,
    and the values are the corresponding populations of those countries.

    Ignore all countries that do not have any population data,
    or population data that cannot be read as an int.

    @rtype: dict[str, int]

    >>> population_data = _get_population_data()
    >>> len(population_data)
    216
    >>> 'Canada' in population_data
    True
    >>> population_data['Canada']
    35543658
    """
    # The first element is ignored.
    _, population_data = _get_json_data(WORLD_BANK_POPULATIONS)
    # First 47 items arent countries, so skips them.
    population_data = population_data[47:]

    countries = {}
    for country in population_data:
        if country['country']['value'] not in countries:
            # Country's key value is a valid population number.
            if country['value'] is not None and int(country['value']) > 0:
                countries[country['country']['value']] = int(country['value'])
    return countries


def _get_region_data():
    """Return country region data from the World Bank.

    The return value is a dictionary, where the keys are region names,
    and the values a list of country names contained in that region.

    Ignore all regions that do not contain any countries.

    @rtype: dict[str, list[str]]

    >>> region_data = _get_region_data()
    >>> len(region_data)
    7
    >>> 'North America' in region_data
    True
    >>> 'Aggregates' in region_data
    False
    """
    _, country_data = _get_json_data(WORLD_BANK_REGIONS)

    regions = {}
    # adds every known region as a key to regions.
    for country in country_data:
        if country["region"]["value"] not in regions:
            if country["region"]["value"].lower() != 'aggregates':
                regions[country["region"]["value"]] = []
    # appends every country to their respective region.
    for country in country_data:
        if country["region"]["value"] in regions:
            regions[country["region"]["value"]] += [country["name"]]
    return regions


def _get_json_data(url):
    """Return a dictionary representing the JSON response from the given url.

    You should not modify this function.

    @type url: str
    @rtype: Dict
    """
    response = request.urlopen(url)
    return json.loads(response.read().decode())


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
