import os
import warnings

from powersimdata.input.usa_tamu_model import TAMU
from powersimdata.input.mat_reader import REISEMATReader
from powersimdata.input.grid_fields \
    import Branch, Bus, DCLine, GenCost, Plant, Storage, Sub


class Grid(object):
    """Grid

    """

    fields = {}
    transform = {}

    def __init__(self, interconnect, source='usa_tamu', engine='REISE'):
        """Constructor

        :param list interconnect: interconnect name(s).
        :param str source: model used to build the network.
        :param str engine: engine used to run scenario, if using MATReader.
        :raises TypeError: if source and engine are not both strings.
        :raises ValueError: if model or engine does not exist.
        :raises NotImplementedError: if engine is not yet built (see REISE.jl).
        """
        if not isinstance(source, str):
            raise TypeError('source must be a string')
        if not isinstance(engine, str):
            got_type = type(engine).__name__
            raise TypeError('engine must be a str, instead got %s' % got_type)

        if source == 'usa_tamu':
            data = TAMU(interconnect)
        elif os.path.splitext(source)[1] == '.mat':
            if engine == 'REISE':
                data = REISEMATReader(source)
            elif engine == 'REISE.jl':
                raise NotImplementedError
            else:
                raise ValueError('Unknown engine %s!' % engine)

        else:
            raise ValueError('%s not implemented' % source)

        # Specific grid info
        self.data_loc = data.data_loc
        self.interconnect = data.interconnect

        # Input data as grid fields
        self.fields['bus'] = Bus(data.bus)
        self.fields['branch'] = Branch(data.branch)
        self.fields['dcline'] = DCLine(data.dcline)
        self.fields['gencost'] = GenCost(data.gencost)
        self.fields['plant'] = Plant(data.plant)
        self.fields['sub'] = Sub(data.sub)
        self.fields['storage'] = Storage(data.storage)

        # Conversion helpers
        self.transform['bus2sub'] = data.bus2sub
        self.transform['zone2id'] = data.zone2id
        self.transform['id2zone'] = data.id2zone
        self.transform['id2type'] = get_id2type()
        self.transform['type2id'] = {value: key for key, value in
                                     self.transform['id2type'].items()}

        # Plotting helper
        self.transform['type2color'] = get_type2color()

    def __getattr__(self, prop_name):
        """
        Overrides the object "." property interface to maintain backwards
        compatibility, i.e. grid.plant
        is the same as grid.fields["plant"], or grid.transform["bus2sub"]

        :param str prop_name: property name as string
        :raises KeyError: For attempts to use key not in the dictionary
        :return: property of the Grid class
        """

        # needed for deepcopy to work
        if prop_name == "__deepcopy__":
            return super().__deepcopy__
        if prop_name == "__len__":
            return super().__len__
        if prop_name == "__getstate__":
            return super().__getstate__
        if prop_name == "__setstate__":
            return super().__setstate__

        # switch between transform and grid_field attributes
        if prop_name in ['bus2sub', 'zone2id', 'id2zone', 'id2type', 
                         'type2id', 'type2color']:
            return self.transform[prop_name]
        else:
            try:
                warnings.warn(
                    "Grid property access is moving to dictionary indexing, "
                    "i.e. grid['branch'] consistent with REISE.jl",
                    DeprecationWarning
                )
                return self.fields[prop_name].data
            except AttributeError as e:
                print(e)

    def __getitem__(self, field_name):
        """
        Allows indexing into the resources dictionary directly from the
        object variable, i.e. grid["plant"] is the
        same as grid.fields["plant"]
        :param str field_name: grid field name as string
        :raises KeyError: For attempts to use key not in the dictionary
        :return: property of the Grid class
        """
        try:
            return self.fields[field_name].data
        except KeyError as e:
            print(e)


def get_type2color():
    """Defines generator type to generator color mapping. Used for plotting.

    :return: (*dict*) -- generator type to color mapping.
    """
    type2color = {
        'wind': "xkcd:green",
        'solar': "xkcd:amber",
        'hydro': "xkcd:light blue",
        'ng': "xkcd:orchid",
        'nuclear': "xkcd:silver",
        'coal': "xkcd:light brown",
        'geothermal': "xkcd:hot pink",
        'dfo': "xkcd:royal blue",
        'biomass': "xkcd:dark green",
        'other': "xkcd:melon",
        'storage': "xkcd:orange"}
    return type2color


def get_id2type():
    """Defines generator type to generator id mapping.

    :return: (*tuple*) -- generator type to generator id mapping.
    """
    id2type = {
        0: 'wind',
        1: 'solar',
        2: 'hydro',
        3: 'ng',
        4: 'nuclear',
        5: 'coal',
        6: 'geothermal',
        7: 'dfo',
        8: 'biomass',
        9: 'other',
        10: 'storage'}
    return id2type
