import unittest
import pandas as pd

from powersimdata.design.scenario_info import ScenarioInfo
from powersimdata.tests.mock_scenario import MockScenario

mock_plant = {
    "plant_id": [101, 102, 103, 104, 105, 106],
    "bus_id": [1001, 1002, 1003, 1004, 1005, 1006],
    "type": ["solar", "wind", "ng", "coal", "dfo", "hydro"],
    "zone_name": ["zone1", "zone2", "zone2", "zone1", "zone1", "zone1"],
    "GenFuelCost": [0, 0, 3.3, 4.4, 5.5, 0],
    "Pmin": [0, 0, 0, 0, 0, 0],
    "Pmax": [50, 200, 80, 100, 120, 220],
}

period_num = 25
mock_pg = pd.DataFrame(
    {
        plant_id: [(i + 1) * p for p in range(period_num)]
        for i, plant_id in enumerate(mock_plant["plant_id"])
    }
)
mock_pg.set_index(
    pd.date_range(start="2016-01-01", periods=period_num, freq="H"), inplace=True
)
mock_pg.index.name = "UTC"

mock_demand = pd.concat(
    [
        mock_pg[
            [
                plant_id
                for plant_id, zone_name in zip(
                    mock_plant["plant_id"], mock_plant["zone_name"]
                )
                if zone_name == "zone1"
            ]
        ]
        .sum(axis=1)
        .to_frame(),
        mock_pg[
            [
                plant_id
                for plant_id, zone_name in zip(
                    mock_plant["plant_id"], mock_plant["zone_name"]
                )
                if zone_name == "zone2"
            ]
        ]
        .sum(axis=1)
        .to_frame(),
    ],
    axis=1,
)
mock_demand.columns = [1, 2]

zone1_available_resource = [
    mock_plant["type"][i]
    for i, zone in enumerate(mock_plant["zone_name"])
    if zone == "zone1"
]

zone2_available_resource = [
    mock_plant["type"][i]
    for i, zone in enumerate(mock_plant["zone_name"])
    if zone == "zone2"
]

zone1_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["zone_name"][i] == "zone1"
]
zone2_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["zone_name"][i] == "zone2"
]

solar_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["type"][i] == "solar"
]
wind_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["type"][i] == "wind"
]
ng_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["type"][i] == "ng"
]
coal_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["type"][i] == "coal"
]
dfo_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["type"][i] == "dfo"
]
hydro_plant_id = [
    plant_id
    for i, plant_id in enumerate(mock_plant["plant_id"])
    if mock_plant["type"][i] == "hydro"
]

mock_solar = mock_pg[solar_plant_id] * 2
mock_wind = mock_pg[wind_plant_id] * 4
mock_hydro = mock_pg[hydro_plant_id] * 1.5

start_time = "2016-01-01 00:00:00"
end_time = "2016-01-02 00:00:00"


class TestScenarioInfo(unittest.TestCase):
    def setUp(self):
        scenario = MockScenario(
            grid_attrs={"plant": mock_plant},
            demand=mock_demand,
            pg=mock_pg,
            solar=mock_solar,
            wind=mock_wind,
            hydro=mock_hydro,
        )
        self.scenario_info = ScenarioInfo(scenario)

    def test_get_available_resource(self):
        assert (
            self.scenario_info.get_available_resource("zone1")
            == zone1_available_resource
        )
        assert (
            self.scenario_info.get_available_resource("zone2")
            == zone2_available_resource
        )

    def test_get_demand(self):
        assert (
            self.scenario_info.get_demand("zone1", start_time, end_time)
            == mock_pg[zone1_plant_id].sum().sum()
        )
        assert (
            self.scenario_info.get_demand("zone2", start_time, end_time)
            == mock_pg[zone2_plant_id].sum().sum()
        )

    def test_get_capacity(self):
        with self.assertWarns(UserWarning):
            self.scenario_info.get_capacity("solar", "zone2")
        assert self.scenario_info.get_capacity("solar", "zone1") == 50
        assert self.scenario_info.get_capacity("wind", "zone2") == 200
        assert self.scenario_info.get_capacity("ng", "all") == 80
        assert self.scenario_info.get_capacity("coal", "all") == 100
        assert self.scenario_info.get_capacity("dfo", "all") == 120
        assert self.scenario_info.get_capacity("hydro", "zone1") == 220

    def test_get_generation(self):
        assert (
            self.scenario_info.get_generation("solar", "zone1", start_time, end_time)
            == mock_pg[solar_plant_id].sum().sum()
        )
        assert (
            self.scenario_info.get_generation("wind", "zone2", start_time, end_time)
            == mock_pg[wind_plant_id].sum().sum()
        )
        assert (
            self.scenario_info.get_generation("ng", "all", start_time, end_time)
            == mock_pg[ng_plant_id].sum().sum()
        )
        assert (
            self.scenario_info.get_generation("coal", "all", start_time, end_time)
            == mock_pg[coal_plant_id].sum().sum()
        )
        assert (
            self.scenario_info.get_generation("dfo", "all", start_time, end_time)
            == mock_pg[dfo_plant_id].sum().sum()
        )
        assert (
            self.scenario_info.get_generation("hydro", "zone1", start_time, end_time)
            == mock_pg[hydro_plant_id].sum().sum()
        )

    def test_get_curtailment(self):
        assert self.scenario_info.get_curtailment(
            "solar", "all", start_time, end_time
        ) == round(
            1 - (mock_pg[solar_plant_id].sum().sum() / mock_solar.sum().sum()), 4
        )
        assert self.scenario_info.get_curtailment(
            "wind", "all", start_time, end_time
        ) == round(1 - (mock_pg[wind_plant_id].sum().sum() / mock_wind.sum().sum()), 4)
        assert self.scenario_info.get_curtailment(
            "hydro", "all", start_time, end_time
        ) == round(
            1 - (mock_pg[hydro_plant_id].sum().sum() / mock_hydro.sum().sum()), 4
        )

    def test_get_profile_resource(self):
        assert (
            self.scenario_info.get_profile_resource(
                "solar", "all", start_time, end_time
            )
            == mock_solar.sum().sum()
        )
        assert (
            self.scenario_info.get_profile_resource("wind", "all", start_time, end_time)
            == mock_wind.sum().sum()
        )
        assert (
            self.scenario_info.get_profile_resource(
                "hydro", "all", start_time, end_time
            )
            == mock_hydro.sum().sum()
        )

    def test_get_capacity_factor(self):
        assert self.scenario_info.get_capacity_factor(
            "solar", "all", start_time, end_time
        ) == round(mock_pg[solar_plant_id].sum().sum() / (50 * period_num), 4)
        assert self.scenario_info.get_capacity_factor(
            "wind", "all", start_time, end_time
        ) == round(mock_pg[wind_plant_id].sum().sum() / (200 * period_num), 4)
        assert self.scenario_info.get_capacity_factor(
            "ng", "all", start_time, end_time
        ) == round(mock_pg[ng_plant_id].sum().sum() / (80 * period_num), 4)
        assert self.scenario_info.get_capacity_factor(
            "coal", "all", start_time, end_time
        ) == round(mock_pg[coal_plant_id].sum().sum() / (100 * period_num), 4)
        assert self.scenario_info.get_capacity_factor(
            "dfo", "all", start_time, end_time
        ) == round(mock_pg[dfo_plant_id].sum().sum() / (120 * period_num), 4)
        assert self.scenario_info.get_capacity_factor(
            "hydro", "all", start_time, end_time
        ) == round(mock_pg[hydro_plant_id].sum().sum() / (220 * period_num), 4)

    def test_get_no_congest_capacity_factor(self):
        assert self.scenario_info.get_no_congest_capacity_factor(
            "solar", "all", start_time, end_time
        ) == round(mock_solar.sum().sum() / (50 * period_num), 4)
        assert self.scenario_info.get_no_congest_capacity_factor(
            "wind", "all", start_time, end_time
        ) == round(mock_wind.sum().sum() / (200 * period_num), 4)
        assert self.scenario_info.get_no_congest_capacity_factor(
            "hydro", "all", start_time, end_time
        ) == round(mock_hydro.sum().sum() / (220 * period_num), 4)
