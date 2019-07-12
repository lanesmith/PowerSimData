# PowerSimData
This package enables communication with the server to carry out power-flow study
in the U.S. electrical grid. State pattern is used to alter the behavior of the
 `Scenario` object when its internal state changes. The following state have
 been implemented so far:
* **create**;
* **execute**;
* **analyze**;
* **delete**.

When a `Scenario` object is created, its state is set either to **create**,
**execute** or **analyze**. This is handled in the constructor of the *Scenario*
class. Only one argument is required to instantiate a `Scenario` object: the
**descriptor** (as `str`) of the scenario, which can either be the scenario id
or name. An empty `str` instantiates the `Scenario` object in the **create**
state. A valid scenario id or name activates the **analyze** state if the
simulation has been successfully ran and the output data have been extracted.
Otherwise the **execute** state is selected.

Once the scenario is created, the internal state of the `Scenario` object is
automatically changed to **execute**. The later state does the heavy lifting: i)
it prepares the simulation inputs, ii) launches the simulation and iii) converts
the MATLAB binaries output files generated by MATPOWER to data frames saved as
Python pickle file. When this is done, the user can activate the **analyze**
state an download input (grid and various profiles used in the simulation) and
output data (power produced by generators and flowing in the branches of the
network). The **delete** state is only accessible from the **analyze** state and
lets the user delete the current scenario, i.e., input and out output data as
well as all references to the scenario in monitoring files.



## 1. Scenario Manipulation
This section illustrates the functionalities of the `Scenario` object.


### A. Analyzing Scenario
The following code snippet shows how one can access scenario information and
data using the `Scenario` object.
```python
from powersimdata.scenario.scenario import Scenario

scenario = Scenario('0')
print(scenario.state.name)  # print name of Scenario object state

scenario.state.print_scenario_info()  # print scenario information
scenario.state.print_infeasibilities()  # print eventual infeasibilities

ct = scenario.state.get_ct  # get change table
grid = scenario.state.get_grid()  # get grid

demand = scenario.state.get_demand()  # get demand profile
hydro = scenario.state.get_hydro()  # get hydro profile
solar = scenario.state.get_solar()  # get solar profile
wind = scenario.state.get_wind()  # get wind profile

pg = scenario.state.get_pg()  # get PG profile
pf = scenario.state.get_pf()  # get PF profile
```
If the capacity of some generators, branches or DC line have been increased
and/or the demand in one or multiple load zones has been scaled for this
scenario then the change table will enclose these changes and the retrieved
grid and input profiles will be modified accordingly.


### B. Creating Scenario
A scenario can be created using few lines of code. This is illustrated below:
```python
from powersimdata.scenario.scenario import Scenario

scenario = Scenario('')
print(scenario.state.name)  # print name of Scenario object state


scenario.state.set_builder(['Western'])  # set interconnection

scenario.state.builder.set_name('test', 'dummy')  # set plan and scenario names
scenario.state.builder.set_time('2016-08-01 00:00:00', '2016-08-31 23:00:00',
                                '124H')  # set start date, end date and interval
scenario.state.builder.set_base_profile('demand', 'v3')  # set demand
scenario.state.builder.set_base_profile('hydro', 'v1')  # set hydro
scenario.state.builder.set_base_profile('solar', 'v2')  # set solar
scenario.state.builder.set_base_profile('wind', 'v1')  # set wind

# scale capacity of solar plants in WA and AZ by 5 and 2.5, respectively
scenario.state.builder.change_table.scale_plant_capacity('solar',
                                                         zone={'Washington': 5,
                                                               'Arizona': 2.5})
# scale capacity of wind farms in OR and MT by 1.5 and 2, respectively
scenario.state.builder.change_table.scale_plant_capacity('wind',
                                                         zone={'Oregon': 1.5,
                                                               'Montana': 2})
# scale capacity of solar plants in NV and WY by 2
scenario.state.builder.change_table.scale_branch_capacity(zone={'Nevada': 2,
                                                                'Wyoming': 2})
print(scenario.state.builder.change_table.ct)  # print change table


# Create scenario
scenario.state.print_scenario_info()  # review information
scenario.state.create_scenario()  # create
print(scenario.state.name)  # print name of Scenario object state
scenario.state.print_scenario_status()  # print status of scenario
```
Once the scenario is successfully created, the state of the `Scenario` object is
switched to **execute**. Also a scenario id is automatically created and printed
on screen


### C. Executing Scenario
It is possible to execute the scenario immediately after the scenario has been
created. One can also create a new `Scenario` object. This is the option we
follow here.

The **execute** state accomplishes the three following tasks.
1. It prepares the simulation inputs: the scaled profiles and MATPOWER case file
enclosing information on the electrical grid that will be used in the
simulation.
2. It launches the simulation. The status of the simulation can be accessed
using the `print_scenario_status` method. Once the status switched from
**running** to **finished**, output data can be extracted. It is worth noting
that. It is possible after the simulation is finished to access the written
output and error messages as demonstrated below.
3. It extracts the output data. This operation can only be done once after the
simulation has finished running.
```python
from powersimdata.scenario.scenario import Scenario

scenario = Scenario('dummy')
scenario.print_scenario_info()  # print scenario information

# prepare simulation inputs
scenario.state.prepare_simulation_input()

# launch simulation
process_run = scenario.state.launch_simulation()

# Get simulation status
scenario.state.print_scenario_status()

# Get output/error messages once the simulation is done running
output_run = process_run.stdout.read()
print(list(filter(None, output_run.decode("utf-8").splitlines())))
error_run = process_run.stderr.read()
print(list(filter(None, error_run.decode("utf-8").splitlines())))

# Extract data
process_extract = scenario.state.extract_simulation_output()
```


### D. Deleting Scenario
A scenario can be deleted. All the input and output files as well as any entries
in monitoring files will be removed. The **delete** state is only accessible
from the **analyze** state.
```python
from powersimdata.scenario.scenario import Scenario
from powersimdata.scenario.delete import Delete

scenario = Scenario('dummy')
print(scenario.state.name)  # print name of Scenario object state
print(scenario.state.allowed)  # print list of accessible states

scenario.change(Delete)
print(scenario.state.name)  # print name of Scenario object state

# Delete scenario
scenario.state.delete_scenario()
```
After the `delete_scenario` method is called, the state of the `Scenario` object
is changed automatically to **create**.


## 2. U.S. Electric Grid and Interconnection
The `Grid` object encapsulates all the information related to the synthetic
network used in this project for a single interconnection (**Eastern**,
**Texas** or **Western**), a combination of two interconnections (**Eastern**
and **Texas** for example) or the full U.S. electric grid (**USA**). Only one
argument is required to instantiate a `Grid` object, a `list` of interconnection
(as `str`).
```python
from powersimdata.input.grid import Grid
western_texas = Grid(['Western', 'Texas'])  # order in list does not matter
```
The object has various attributes. These are listed below along with a short
description:
* **zone2id (id2zone)**: `dict` -- load zone name (load zone id) to load zone id
(load zone name).
* **type2id** (**id2type**): `dict` -- generator type (id) to generator id
(type).
* **type2color**: `dict` -- generator type to generator color as used in plots.
* **interconnect**: `str` --  interconnection name.
* **bus**: `pandas.DataFrame` -- bus id as index and bus characteristics as
columns.
* **sub**: `pandas.DataFrame` -- substation id as index and substation
information as columns.
* **bus2sub**: `pandas.DataFrame` -- bus id as index and substation id as
column.
* **plant**: `pandas.DataFrame` -- plant id as index and plant characteristics
as columns.
* **branch**: `pandas.DataFrame` -- branch id as index and branch
characteristics as columns.
* **gencost**: `pandas.DataFrame` -- plant id as index and generation cost
information as columns.
* **dcline**: `pandas.DataFrame` -- DC line id as index and DC line
characteristics as columns.
```python
from powersimdata.input.grid import Grid
usa = Grid(['USA'])
usa.plant.head()
wind_farm = usa.plant.groupby('type').get_group('wind')  # wind farm in network
dcline = usa.dcline  # DC line in network
```

---
**NOTE**

Discrepancies were found between the branch data frame and ***.aux*** files
from <https://electricgrids.engr.tamu.edu>.

The branch attribute of the `Grid` object was merged with the branch data found
in the ***.aux*** files for the three interconnects: Eastern is 
***ActivSg70k.aux***, Western is ***ActivSg2000.aux***, and Texas is
***ActivSg10k.aux***. A new column *branch_device_type* has been added in
the branch data frame from the ***.aux*** files. It is a categorical attribute
with three values: Line, Transformer, and TransformerWinding. Several
discrepancies between the branch attribute of the `Grid` object and the
***.aux*** files, were observed:


| interconnect  | from_bus_id   |  to_bus_id    |  discrepancy: description and resolution                                                          |
| ------------- |:-------------:|:-------------:|:-------------------------------------------------------------------------------------------------:|
| Eastern       | 6991          | 13525         | Not in ***.aux***. Distance and ratio --> classified as Line.                                     |
| Eastern       | 54736         | 56767         | Not in ***.aux***. Distance and ratio --> classified as Line.                                     |
| Eastern       | 30322         | 30839         | from_bus_id and to_bus_id switched in ***.aux***                                                  |
| Eastern       | 30304         | 30310         | In ***.aux*** but not in `Grid` object --> Not added.                                             |
| Texas         | 3007161       | 3007292       | Multiple in ***.aux*** as Line and Transformer. Ratio 0 and 1. Distance >0 --> classified as Line |

---