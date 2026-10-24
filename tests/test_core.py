"""Offline tests for registry, normalisers, validation and storage (stdlib unittest)."""

import datetime as dt
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd

from labobs import connectors as C
from labobs import storage
from labobs.registry import load_registry
from labobs.validate import validate


class TestRegistry(unittest.TestCase):
    def test_registry_loads(self):
        reg = load_registry()
        self.assertGreater(len(reg), 5)
        for s in reg.values():
            for d in s.datasets:
                self.assertIn(d.connector, C.CONNECTORS, d.key)


class TestNormalisers(unittest.TestCase):
    def test_worldbank(self):
        rows = [{"country": {"id": "AU", "value": "Australia"}, "countryiso3code": "AUS",
                 "indicator": {"id": "SL.UEM.TOTL.ZS"}, "date": "2024", "value": 4.1}]
        df = C.norm_worldbank(json.dumps(rows).encode(), {})
        self.assertEqual(df.loc[0, "ref_area"], "AUS")
        self.assertEqual(df.loc[0, "value"], 4.1)

    def test_ilostat_gz(self):
        csv = b"ref_area,source,indicator,sex,classif1,time,obs_value\nAUS,X,UNE,SEX_T,AGE_YTHADULT_Y15-24,2024,9.5\n"
        df = C.norm_ilostat(gzip.compress(csv), {})
        self.assertEqual(list(df[["ref_area", "period", "value"]].iloc[0]), ["AUS", 2024, 9.5])

    def test_sdmx_eurostat_style(self):
        csv = b"DATAFLOW,LAST UPDATE,freq,s_adj,age,unit,sex,geo,TIME_PERIOD,OBS_VALUE,OBS_FLAG\nESTAT:UNE_RT_M(1.0),x,M,SA,Y_LT25,PC_ACT,T,ES,2026-07,22.9,\n"
        df = C.norm_sdmx(csv, {"dataflow": "une_rt_m"})
        self.assertEqual(df.loc[0, "ref_area"], "ES")
        self.assertEqual(df.loc[0, "period"], "2026-07")
        self.assertEqual(df.loc[0, "indicator"], "une_rt_m")

    def test_bls_periods(self):
        self.assertEqual(C._bls_period("2026", "M08"), "2026-08")
        self.assertEqual(C._bls_period("2026", "Q02"), "2026-Q2")
        self.assertIsNone(C._bls_period("2026", "S01"))
        payload = [{"seriesID": "LNS14000000", "data": [
            {"year": "2026", "period": "M09", "value": "4.3", "footnotes": [{}]},
            {"year": "2026", "period": "M08", "value": "4.2", "footnotes": [{"code": "P"}]}]}]
        df = C.norm_bls(json.dumps(payload).encode(), {"labels": {"LNS14000000": "UR"}})
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["period"], "2026-08")

    def test_fred(self):
        payload = {"UNRATE": "observation_date,UNRATE\n2026-08-01,4.2\n2026-09-01,.\n"}
        df = C.norm_fred(json.dumps(payload).encode(), {})
        self.assertTrue(pd.isna(df.iloc[1]["value"]))


class TestValidate(unittest.TestCase):
    base = pd.DataFrame({"ref_area": ["AUS", "USA"], "indicator": ["u", "u"],
                         "period": ["2026-08", "2026-08"], "value": [4.2, 4.3]})

    def test_first_vintage(self):
        r = validate(self.base, None)
        self.assertTrue(r.ok)
        self.assertTrue(r.stats["first_vintage"])

    def test_missing_columns(self):
        self.assertFalse(validate(self.base.drop(columns=["value"]), None).ok)

    def test_truncation_rejected(self):
        big = pd.concat([self.base] * 10, ignore_index=True)
        big["period"] = [f"2026-{i:02d}" for i in range(1, 21)][:len(big)]
        self.assertFalse(validate(self.base, big).ok)

    def test_revision_and_addition(self):
        new = pd.concat([self.base, pd.DataFrame({"ref_area": ["AUS"], "indicator": ["u"],
                                                   "period": ["2026-09"], "value": [4.1]})])
        new.loc[0, "value"] = 4.3
        r = validate(new.reset_index(drop=True), self.base)
        self.assertEqual(r.stats["added"], 1)
        self.assertEqual(r.stats["revised"], 1)


class TestStorage(unittest.TestCase):
    def test_vintage_dedup(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with mock.patch.object(storage, "DATA_DIR", tmp), \
                 mock.patch.object(storage, "MANIFEST", tmp / "manifest.json"):
                d = dt.date(2026, 10, 24)
                new, meta = storage.store_raw("employment", "s", "d", b"abc", "csv", "u", "open", d)
                self.assertTrue(new and meta["payload_committed"])
                new2, _ = storage.store_raw("employment", "s", "d", b"abc", "csv", "u", "open", d)
                self.assertFalse(new2)
                new3, meta3 = storage.store_raw("employment", "s", "d", b"abcd", "csv", "u", "restricted",
                                                dt.date(2026, 10, 25))
                self.assertTrue(new3)
                self.assertFalse(meta3["payload_committed"])
                self.assertEqual(meta3["previous_vintage"], "2026-10-24")


if __name__ == "__main__":
    unittest.main()
