import numpy as np
from openmdao.api import ExplicitComponent
from six import string_types

from openmdoc.phases.grid_data import GridData
from openmdoc.utils.misc import get_rate_units


class CollocationComp(ExplicitComponent):

    """
    CollocationComp computes the generalized defect of a segment for implicit collocation.
    The defect is the interpolated state derivative at the collocation nodes minus
    the computed state derivative at the collocation nodes.
    """
    def initialize(self):

        self.metadata.declare(
            'grid_data', types=GridData,
            desc='Container object for grid info')

        self.metadata.declare(
            'state_options', types=dict,
            desc='Dictionary of state names/options for the phase')

        self.metadata.declare(
            'time_units', default=None, allow_none=True, types=string_types,
            desc='Units of time')

    def setup(self):
        gd = self.metadata['grid_data']
        num_col_nodes = gd.subset_num_nodes['col']
        time_units = self.metadata['time_units']
        state_options = self.metadata['state_options']

        self.var_names = var_names = {}
        for state_name in state_options:
            var_names[state_name] = {
                'f_approx': 'f_approx:{0}'.format(state_name),
                'f_computed': 'f_computed:{0}'.format(state_name),
                'defect': 'defects:{0}'.format(state_name),
            }

        for state_name, options in state_options.items():
            shape = options['shape']
            units = options['units']

            rate_units = get_rate_units(units, time_units)
            var_names = self.var_names[state_name]

            self.add_input(
                name=var_names['f_approx'],
                shape=(num_col_nodes,) + shape,
                desc='Estimated derivative of state {0} '
                     'at the collocation nodes'.format(state_name),
                units=rate_units)

            self.add_input(
                name=var_names['f_computed'],
                shape=(num_col_nodes,) + shape,
                desc='Computed derivative of state {0} '
                     'at the collocation nodes'.format(state_name),
                units=rate_units)

            self.add_output(
                name=var_names['defect'],
                shape=(num_col_nodes,) + shape,
                desc='Interior defects of state {0}'.format(state_name),
                units=rate_units)

            if 'defect_scaler' in options:
                def_scl = options['defect_scaler']
            else:
                def_scl = 1.0

            self.add_constraint(name=var_names['defect'],
                                equals=0.0,
                                scaler=def_scl)

        # Setup partials
        num_col_nodes = self.metadata['grid_data'].subset_num_nodes['col']
        state_options = self.metadata['state_options']

        for state_name, options in state_options.items():
            shape = options['shape']
            arange = np.arange(num_col_nodes * np.prod(shape))

            var_names = self.var_names[state_name]

            self.declare_partials(of=var_names['defect'],
                                  wrt=var_names['f_approx'],
                                  rows=arange,
                                  cols=arange,
                                  val=1.0)

            self.declare_partials(of=var_names['defect'],
                                  wrt=var_names['f_computed'],
                                  rows=arange,
                                  cols=arange,
                                  val=-1.0)

    def compute(self, inputs, outputs):
        state_options = self.metadata['state_options']

        for state_name in state_options:
            var_names = self.var_names[state_name]

            f_approx = inputs[var_names['f_approx']]
            f_computed = inputs[var_names['f_computed']]
            outputs[var_names['defect']] = f_approx - f_computed
