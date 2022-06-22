from django.test import TestCase

from stats.tables import (ASPlayerHittingGameStatsTable,
    ASPlayerPitchingGameStatsTable, PlayerHittingStatsTable,
    PlayerHittingStatsTable2, PlayerPageHittingStatsTable,
    PlayerPageHittingStatsSplitsTable, PlayerPageGameHittingStatsSplitsTable,
    PlayerPitchingStatsTable, StandingsTable,
    TeamGameLineScoreTable, TeamHittingStatsTable, TeamPitchingStatsTable)

from stats.stat_calc import (_convert_to_str, _convert_to_str_ip,
    _convert_to_str_pitching,)

class TableStatObject():
    def __init__(self):
        self.average = 0.650
        self.on_base_percentage = 0.450
        self.slugging_percentage = 0.500
        self.on_base_plus_slugging = 1.000

        self.era = 3.67
        self.whip = 1.25
        self.innings_pitched = 67.67

class ASPlayerHittingGameStatsTableTest(TestCase):
    """
    Tests ASPlayerHittingGameStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = ASPlayerHittingGameStatsTable({})
        cls.record = TableStatObject()
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record.average)
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):
        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record.on_base_percentage)
        self.assertEqual(record_obp, obp)
    
    def test_render_slugging_percentage(self):
        slg = self.table.render_slugging_percentage(self.record)
        record_slg = _convert_to_str(self.record.slugging_percentage)
        self.assertEqual(record_slg, slg)

    def test_render_on_base_plus_slugging(self):
        ops = self.table.render_on_base_plus_slugging(self.record)
        record_ops = _convert_to_str(self.record.on_base_plus_slugging)
        self.assertEqual(record_ops, ops)



class ASPlayerPitchingGameStatsTableTest(TestCase):
    """
    Tests ASPlayerPitchingGameStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = ASPlayerPitchingGameStatsTable({})
        cls.record = TableStatObject()
        return super().setUpTestData()

    def test_render_era(self):
        era = self.table.render_era(self.record)
        record_era = _convert_to_str_pitching(self.record.era)
        self.assertEqual(record_era, era)

    def test_render_whip(self):
        whip = self.table.render_whip(self.record)
        record_whip = _convert_to_str_pitching(self.record.whip)
        self.assertEqual(record_whip, whip)

    def test_render_innings_pitched(self):
        ip = self.table.render_innings_pitched(self.record)
        record_ip = _convert_to_str_ip(self.record.innings_pitched)
        self.assertEqual(record_ip, ip)


class TeamHittingStatsTableTest(TestCase):
    """
    Tests TeamHittingStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = TeamHittingStatsTable({})
        cls.record = {
            "average": 0.350,
            "on_base_percentage":0.650
            }
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record["average"])
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):

        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record["on_base_percentage"])
        self.assertEqual(record_obp, obp)


class PlayerHittingStatsTableTest(TestCase):
    """
    Tests PlayerHittingStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = PlayerHittingStatsTable({})
        cls.record = {
            "average": 0.350,
            "on_base_percentage":0.650
            }
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record["average"])
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):

        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record["on_base_percentage"])
        self.assertEqual(record_obp, obp)


class PlayerHittingStatsTable2Test(TestCase):
    """
    #potentially deprecated table?
    Tests PlayerHittingStatsTable2 from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = PlayerHittingStatsTable2({})
        cls.record = {
            "average": 0.350,
            "on_base_percentage":0.650
            }
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record["average"])
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):

        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record["on_base_percentage"])
        self.assertEqual(record_obp, obp)


class PlayerPitchingStatsTableTest(TestCase):
    """
    Tests PlayerPitchingStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = PlayerPitchingStatsTable({})
        cls.record = {
            "era": 3.350,
            "whip":1.650,
            "innings_pitched": 67.67
            }
        return super().setUpTestData()

    def test_render_era(self):
        era = self.table.render_era(self.record)
        record_era = _convert_to_str_pitching(self.record["era"])
        self.assertEqual(record_era, era)

    def test_render_whip(self):
        whip = self.table.render_whip(self.record)
        record_whip = _convert_to_str_pitching(self.record["whip"])
        self.assertEqual(record_whip, whip)

    def test_render_innings_pitched(self):
        ip = self.table.render_innings_pitched(self.record)
        record_ip = _convert_to_str_ip(self.record["innings_pitched"])
        self.assertEqual(record_ip, ip)


class TeamPitchingStatsTableTest(TestCase):
    """
    Tests TeamPitchingStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = TeamPitchingStatsTable({})
        cls.record = {
            "era": 3.350,
            "whip":1.650,
            "innings_pitched": 67.67
            }
        return super().setUpTestData()

    def test_render_era(self):
        era = self.table.render_era(self.record)
        record_era = _convert_to_str_pitching(self.record["era"])
        self.assertEqual(record_era, era)

    def test_render_whip(self):
        whip = self.table.render_whip(self.record)
        record_whip = _convert_to_str_pitching(self.record["whip"])
        self.assertEqual(record_whip, whip)

    def test_render_innings_pitched(self):
        ip = self.table.render_innings_pitched(self.record)
        record_ip = _convert_to_str_ip(self.record["innings_pitched"])
        self.assertEqual(record_ip, ip)



class StandingsTableTest(TestCase):
    """
    Tests StandingsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = StandingsTable({})
        cls.record = {
            "win": 2,
            "loss":3,
            "tie": 0,
            "pct": 0.667
            }
        return super().setUpTestData()

    def test_render_win(self):
        win = self.table.render_win(self.record)
        record_win = str(self.record["win"])
        self.assertEqual(record_win, win)

    def test_render_loss(self):
        loss = self.table.render_loss(self.record)
        record_loss = str(self.record["loss"])
        self.assertEqual(record_loss, loss)

    def test_render_tie(self):
        tie = self.table.render_tie(self.record)
        record_tie = str(self.record["tie"])
        self.assertEqual(record_tie, tie)

    def test_render_pct(self):
        pct = self.table.render_pct(self.record)
        record_pct = _convert_to_str(self.record["pct"])
        self.assertEqual(record_pct, pct)


class PlayerPageHittingStatsTableTest(TestCase):
    """
    Tests PlayerPageHittingStatsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = PlayerPageHittingStatsTable({})
        cls.record = {
            "average": 0.350,
            "on_base_percentage":0.650
            }
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record["average"])
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):
        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record["on_base_percentage"])
        self.assertEqual(record_obp, obp)


class PlayerPageHittingStatsSplitsTableTest(TestCase):
    """
    Tests PlayerPageHittingStatsSplitsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = PlayerPageHittingStatsSplitsTable({})
        cls.record = {
            "average": 0.350,
            "on_base_percentage":0.650
            }
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record["average"])
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):
        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record["on_base_percentage"])
        self.assertEqual(record_obp, obp)


class PlayerPageGameHittingStatsSplitsTableTest(TestCase):
    """
    Tests PlayerPageGameHittingStatsSplitsTable from stats/tables.py

    Used to mainly test the render_<stat_name> method that don't get tested.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.table = PlayerPageGameHittingStatsSplitsTable({})
        cls.record = {
            "average": 0.350,
            "on_base_percentage":0.650
            }
        return super().setUpTestData()

    def test_render_average(self):
        average = self.table.render_average(self.record)
        record_average = _convert_to_str(self.record["average"])
        self.assertEqual(record_average, average)

    def test_render_on_base_percentage(self):
        obp = self.table.render_on_base_percentage(self.record)
        record_obp = _convert_to_str(self.record["on_base_percentage"])
        self.assertEqual(record_obp, obp)

    