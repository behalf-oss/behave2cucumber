import unittest
import b2c
import json
import os

BEHAVE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/behave.json"
EXPECTED_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/expected.json"
class TestB2C(unittest.TestCase):

    def test_convert(self):
        with open(BEHAVE_JSON) as f:
            converted = b2c.convert(json.load(f))
        
        with open(EXPECTED_JSON) as f:
            expected_result = json.load(f)

        assert (sorted(converted) == sorted(expected_result))
        
if __name__ == '__main__':
    unittest.main()
