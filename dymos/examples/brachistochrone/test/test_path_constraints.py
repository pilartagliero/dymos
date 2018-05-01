from __future__ import print_function, absolute_import, division

import itertools
import unittest

from parameterized import parameterized


class TestBrachistochronePathConstraints(unittest.TestCase):

    def test_control_rate_path_constraint_gl(self):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from openmdao.api import Problem, Group, ScipyOptimizeDriver, CSCJacobian, DirectSolver
        from openmdao.utils.assert_utils import assert_rel_error
        from dymos import Phase
        from dymos.examples.brachistochrone.brachistochrone_ode import BrachistochroneODE

        p = Problem(model=Group())
        p.driver = ScipyOptimizeDriver()

        phase = Phase('gauss-lobatto',
                      ode_class=BrachistochroneODE,
                      num_segments=10)

        p.model.add_subsystem('phase0', phase)

        phase.set_time_options(initial_bounds=(0, 0), duration_bounds=(.5, 10))

        phase.set_state_options('x', fix_initial=True, fix_final=True)
        phase.set_state_options('y', fix_initial=True, fix_final=True)
        phase.set_state_options('v', fix_initial=True)

        phase.add_control('theta', units='deg', dynamic=True,
                          rate_continuity=False, lower=0.01, upper=179.9)

        phase.add_control('g', units='m/s**2', dynamic=False, opt=False, val=9.80665)

        # Minimize time at the end of the phase
        phase.add_objective('time', loc='final', scaler=10)

        phase.add_path_constraint('theta_rate', lower=0, upper=100, units='deg/s')

        p.model.jacobian = CSCJacobian()
        p.model.linear_solver = DirectSolver()

        p.setup(mode='rev')

        p['phase0.t_initial'] = 0.0
        p['phase0.t_duration'] = 2.0

        p['phase0.states:x'] = phase.interpolate(ys=[0, 10], nodes='disc')
        p['phase0.states:y'] = phase.interpolate(ys=[10, 5], nodes='disc')
        p['phase0.states:v'] = phase.interpolate(ys=[0, 9.9], nodes='disc')
        p['phase0.controls:theta'] = phase.interpolate(ys=[5, 100.5], nodes='all')

        # Solve for the optimal trajectory
        p.run_driver()

        # Test the results
        assert_rel_error(self, phase.get_values('time')[-1], 1.8016, tolerance=1.0E-3)

    def test_control_rate2_path_constraint_gl(self):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from openmdao.api import Problem, Group, ScipyOptimizeDriver, CSCJacobian, DirectSolver
        from openmdao.utils.assert_utils import assert_rel_error
        from dymos import Phase
        from dymos.examples.brachistochrone.brachistochrone_ode import BrachistochroneODE

        p = Problem(model=Group())
        p.driver = ScipyOptimizeDriver()

        phase = Phase('gauss-lobatto',
                      ode_class=BrachistochroneODE,
                      num_segments=10,
                      transcription_order=5)

        p.model.add_subsystem('phase0', phase)

        phase.set_time_options(initial_bounds=(0, 0), duration_bounds=(.5, 10))

        phase.set_state_options('x', fix_initial=True, fix_final=True)
        phase.set_state_options('y', fix_initial=True, fix_final=True)
        phase.set_state_options('v', fix_initial=True)

        phase.add_control('theta', units='deg', dynamic=True,
                          rate_continuity=False, lower=0.01, upper=179.9)

        phase.add_control('g', units='m/s**2', dynamic=False, opt=False, val=9.80665)

        # Minimize time at the end of the phase
        phase.add_objective('time', loc='final', scaler=10)

        phase.add_path_constraint('theta_rate2', lower=-200, upper=200, units='rad/s**2')

        p.model.jacobian = CSCJacobian()
        p.model.linear_solver = DirectSolver()

        p.setup(mode='rev')

        p['phase0.t_initial'] = 0.0
        p['phase0.t_duration'] = 2.0

        p['phase0.states:x'] = phase.interpolate(ys=[0, 10], nodes='disc')
        p['phase0.states:y'] = phase.interpolate(ys=[10, 5], nodes='disc')
        p['phase0.states:v'] = phase.interpolate(ys=[0, 9.9], nodes='disc')
        p['phase0.controls:theta'] = phase.interpolate(ys=[5, 100.5], nodes='all')

        # Solve for the optimal trajectory
        p.run_driver()

        # Test the results
        assert_rel_error(self, phase.get_values('time')[-1], 1.8016, tolerance=1.0E-3)

    def test_control_rate_path_constraint_radau(self):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from openmdao.api import Problem, Group, ScipyOptimizeDriver, CSCJacobian, DirectSolver
        from openmdao.utils.assert_utils import assert_rel_error
        from dymos import Phase
        from dymos.examples.brachistochrone.brachistochrone_ode import BrachistochroneODE

        p = Problem(model=Group())
        p.driver = ScipyOptimizeDriver()

        phase = Phase('radau-ps',
                      ode_class=BrachistochroneODE,
                      num_segments=10)

        p.model.add_subsystem('phase0', phase)

        phase.set_time_options(initial_bounds=(0, 0), duration_bounds=(.5, 10))

        phase.set_state_options('x', fix_initial=True, fix_final=True)
        phase.set_state_options('y', fix_initial=True, fix_final=True)
        phase.set_state_options('v', fix_initial=True)

        phase.add_control('theta', units='deg', dynamic=True,
                          rate_continuity=False, lower=0.01, upper=179.9)

        phase.add_control('g', units='m/s**2', dynamic=False, opt=False, val=9.80665)

        # Minimize time at the end of the phase
        phase.add_objective('time', loc='final', scaler=10)

        phase.add_path_constraint('theta_rate', lower=0, upper=100, units='deg/s')

        p.model.jacobian = CSCJacobian()
        p.model.linear_solver = DirectSolver()

        p.setup(mode='rev')

        p['phase0.t_initial'] = 0.0
        p['phase0.t_duration'] = 2.0

        p['phase0.states:x'] = phase.interpolate(ys=[0, 10], nodes='disc')
        p['phase0.states:y'] = phase.interpolate(ys=[10, 5], nodes='disc')
        p['phase0.states:v'] = phase.interpolate(ys=[0, 9.9], nodes='disc')
        p['phase0.controls:theta'] = phase.interpolate(ys=[5, 100.5], nodes='all')

        # Solve for the optimal trajectory
        p.run_driver()

        # Test the results
        assert_rel_error(self, phase.get_values('time')[-1], 1.8016, tolerance=1.0E-3)

    def test_control_rate2_path_constraint_radau(self):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from openmdao.api import Problem, Group, ScipyOptimizeDriver, CSCJacobian, DirectSolver
        from openmdao.utils.assert_utils import assert_rel_error
        from dymos import Phase
        from dymos.examples.brachistochrone.brachistochrone_ode import BrachistochroneODE

        p = Problem(model=Group())
        p.driver = ScipyOptimizeDriver()

        phase = Phase('radau-ps',
                      ode_class=BrachistochroneODE,
                      num_segments=10,
                      transcription_order=5)

        p.model.add_subsystem('phase0', phase)

        phase.set_time_options(initial_bounds=(0, 0), duration_bounds=(.5, 10))

        phase.set_state_options('x', fix_initial=True, fix_final=True)
        phase.set_state_options('y', fix_initial=True, fix_final=True)
        phase.set_state_options('v', fix_initial=True)

        phase.add_control('theta', units='deg', dynamic=True,
                          rate_continuity=False, lower=0.01, upper=179.9)

        phase.add_control('g', units='m/s**2', dynamic=False, opt=False, val=9.80665)

        # Minimize time at the end of the phase
        phase.add_objective('time', loc='final', scaler=10)

        phase.add_path_constraint('theta_rate2', lower=-200, upper=200, units='rad/s**2')

        p.model.jacobian = CSCJacobian()
        p.model.linear_solver = DirectSolver()

        p.setup(mode='rev')

        p['phase0.t_initial'] = 0.0
        p['phase0.t_duration'] = 2.0

        p['phase0.states:x'] = phase.interpolate(ys=[0, 10], nodes='disc')
        p['phase0.states:y'] = phase.interpolate(ys=[10, 5], nodes='disc')
        p['phase0.states:v'] = phase.interpolate(ys=[0, 9.9], nodes='disc')
        p['phase0.controls:theta'] = phase.interpolate(ys=[5, 100.5], nodes='all')

        # Solve for the optimal trajectory
        p.run_driver()

        # Test the results
        assert_rel_error(self, phase.get_values('time')[-1], 1.8016, tolerance=1.0E-3)