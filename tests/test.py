import unittest
import behave2cucumber
import json
import os

BEHAVE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/behave.json"
EXPECTED_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/expected.json"
AUTORETRY_BEHAVE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/autoretry.json"
AUTORETRY_EXPECTED_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/autoretry_expected.json"
AUTORETRY_DEDUPE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/autoretry_dedupe.json"
class TestB2C(unittest.TestCase):
    def test_convert(self):
        with open(BEHAVE_JSON) as f:
            converted = behave2cucumber.convert(json.load(f))

        with open(EXPECTED_JSON) as f:
            expected_result = json.load(f)

        assert (sorted(converted) == sorted(expected_result))

    def test_autoretry_convert(self):
        with open(AUTORETRY_BEHAVE_JSON) as f:
            converted = behave2cucumber.convert(json.load(f))

        with open(AUTORETRY_EXPECTED_JSON) as f:
            expected_result = json.load(f)

        assert (sorted(converted) == sorted(expected_result))

    def test_dedupe_convert(self):
        with open(AUTORETRY_BEHAVE_JSON) as f:
            converted = behave2cucumber.convert(json.load(f), deduplicate=True)

        with open(AUTORETRY_DEDUPE_JSON) as f:
            expected_result = json.load(f)

        assert (sorted(converted) == sorted(expected_result))

    def test_ids_are_unique(self):
        with open(BEHAVE_JSON) as f:
            converted = behave2cucumber.convert(json.load(f))
            ids = []
            for feature in converted:
                ids.append(feature['id'])
                for element in feature['elements']:
                    ids.append(element['id'])

        assert (len(set(ids)) == 5)


if __name__ == '__main__':
    unittest.main()
