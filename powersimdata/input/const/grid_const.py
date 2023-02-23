# The index name of each data frame
indices = {
    "sub": "sub_id",
    "bus2sub": "bus_id",
    "branch": "branch_id",
    "bus": "bus_id",
    "dcline": "dcline_id",
    "plant": "plant_id",
}

# AC lines
col_name_branch = [
    "from_bus_id",
    "to_bus_id",
    "r",
    "x",
    "b",
    "rateA",
    "rateB",
    "rateC",
    "ratio",
    "angle",
    "status",
    "angmin",
    "angmax",
    "Pf",
    "Qf",
    "Pt",
    "Qt",
    "mu_Sf",
    "mu_St",
    "mu_angmin",
    "mu_angmax",
    "branch_device_type",
    "interconnect",
    "from_zone_id",
    "to_zone_id",
    "from_zone_name",
    "to_zone_name",
    "from_lat",
    "from_lon",
    "to_lat",
    "to_lon",
]
col_type_branch = [
    "int",
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "str",
    "str",
    "int",
    "int",
    "str",
    "str",
    "float",
    "float",
    "float",
    "float",
]


# bus
col_name_bus = [
    "type",
    "Pd",
    "Qd",
    "Gs",
    "Bs",
    "zone_id",
    "Vm",
    "Va",
    "baseKV",
    "loss_zone",
    "Vmax",
    "Vmin",
    "lam_P",
    "lam_Q",
    "mu_Vmax",
    "mu_Vmin",
    "interconnect",
    "eia_id",
    "lat",
    "lon",
]
col_type_bus = [
    "int",
    "float",
    "float",
    "float",
    "float",
    "int",
    "float",
    "float",
    "float",
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "str",
    "float",
    "float",
]


# bus to substations
col_name_bus2sub = ["sub_id", "interconnect"]
col_type_bus2sub = ["int", "str"]


# DC lines
col_name_dcline = [
    "from_bus_id",
    "to_bus_id",
    "status",
    "Pf",
    "Pt",
    "Qf",
    "Qt",
    "Vf",
    "Vt",
    "Pmin",
    "Pmax",
    "QminF",
    "QmaxF",
    "QminT",
    "QmaxT",
    "loss0",
    "loss1",
    "muPmin",
    "muPmax",
    "muQminF",
    "muQmaxF",
    "muQminT",
    "muQmaxT",
    "from_interconnect",
    "to_interconnect",
]
col_type_dcline = [
    "int",
    "int",
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "str",
    "str",
]


# Generation Cost
col_name_gencost = [
    "type",
    "startup",
    "shutdown",
    "n",
    "c2",
    "c1",
    "c0",
    "interconnect",
]
col_type_gencost = ["int", "float", "float", "int", "float", "float", "float", "str"]


# Generator
col_name_plant = [
    "bus_id",
    "Pg",
    "Qg",
    "Qmax",
    "Qmin",
    "Vg",
    "mBase",
    "status",
    "Pmax",
    "Pmin",
    "Pc1",
    "Pc2",
    "Qc1min",
    "Qc1max",
    "Qc2min",
    "Qc2max",
    "ramp_agc",
    "ramp_10",
    "ramp_30",
    "ramp_q",
    "apf",
    "mu_Pmax",
    "mu_Pmin",
    "mu_Qmax",
    "mu_Qmin",
    "type",
    "interconnect",
    "GenFuelCost",
    "GenIOB",
    "GenIOC",
    "GenIOD",
    "zone_id",
    "zone_name",
    "lat",
    "lon",
]
col_type_plant = [
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "str",
    "str",
    "float",
    "float",
    "float",
    "int",
    "int",
    "str",
    "float",
    "float",
]


# substations
col_name_sub = ["name", "interconnect_sub_id", "lat", "lon", "interconnect"]
col_type_sub = ["str", "int", "float", "float", "str"]


# storage
col_name_storage_storagedata = [
    "UnitIdx",
    "InitialStorage",
    "InitialStorageLowerBound",
    "InitialStorageUpperBound",
    "InitialStorageCost",
    "TerminalStoragePrice",
    "MinStorageLevel",
    "MaxStorageLevel",
    "OutEff",
    "InEff",
    "LossFactor",
    "rho",
    "ExpectedTerminalStorageMax",
    "ExpectedTerminalStorageMin",
    "duration",
]
col_type_storage_storagedata = [
    "int",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
    "float",
]