"""Tests for Hoodscore."""
from src.core import Hoodscore
def test_init(): assert Hoodscore().get_stats()["ops"] == 0
def test_op(): c = Hoodscore(); c.process(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Hoodscore(); [c.process() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Hoodscore(); c.process(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Hoodscore(); r = c.process(); assert r["service"] == "hoodscore"
