from unittest import TestCase

import jsonschema

class TestType(TestCase):
    def test_schema(self):
        schema = {
            "type": [
                { "type": "array", "minItems": 10 },
                { "type": "string", "pattern": "^0+$" }
            ]
        }

        data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        data2 = "0"
        data3 = 1203

        for x in [data1, data2]:
            try:
                jsonschema.validate(x, schema)
            except ValueError, e:
                self.fail("Unexpected failure: %s" % e)

        self.assertRaises(ValueError, jsonschema.validate, data3, schema)

    def _test_type(self, typename, valids, invalids):
        for x in valids:
            try:
                jsonschema.validate(x, {"type":typename})
            except ValueError, e:
                self.fail("Unexpected failure: %s" % e)

        for x in invalids:
            self.assertRaises(ValueError, jsonschema.validate, x,
                              {"type":typename})

    def test_integer(self):
        valid_ints = [1, -89, 420000]
        invalid_ints = [1.2, "bad", {"test":"blah"}, [32, 49], None, True]
        self._test_type('integer', valid_ints, invalid_ints)

    def test_string(self):
        valids = ["abc", u"unicode"]
        invalids = [1.2, 1, {"test":"blah"}, [32, 49], None, True]
        self._test_type('string', valids, invalids)

    def test_number(self):
        valids = [1.2, -89.42, 48, -32]
        invalids = ["bad", {"test":"blah"}, [32.42, 494242], None, True]
        self._test_type('number', valids, invalids)

    def test_boolean(self):
        valids = [True, False]
        invalids = [1.2, "False", {"test":"blah"}, [32, 49], None, 1, 0]
        self._test_type('boolean', valids, invalids)

    def test_object(self):
        valids = [{"blah": "test"}, {"this":{"blah":"test"}}, {1:2, 10:20}]
        invalids = [1.2, "bad", 123, [32, 49], None, True]
        self._test_type('object', valids, invalids)

    def test_array(self):
        valids = [[1, 89], [48, {"test":"blah"}, "49", 42]]
        invalids = [1.2, "bad", {"test":"blah"}, 1234, None, True]
        self._test_type('array', valids, invalids)

    def test_null(self):
        valids = [None]
        invalids = [1.2, "bad", {"test":"blah"}, [32, 49], 1284, True]
        self._test_type('null', valids, invalids)

    def test_any(self):
        valids = [1.2, "bad", {"test":"blah"}, [32, 49], None, 1284, True]
        self._test_type('any', valids, [])

    def test_default(self):
        # test default value (same as any really)
        valids = [1.2, "bad", {"test":"blah"}, [32, 49], None, 1284, True]
        for x in valids:
            try:
                jsonschema.validate(x, {})
            except ValueError:
                self.fail("Unexpected failure: %s" % e)

    def test_multi(self):
        types = ["null", "integer", "string"]
        valids = [None, 42, "string"]
        invalids = [1.2, {"test":"blah"}, [32, 49], True]
        self._test_type(types, valids, invalids)


class TestDisallow(TestType):
    def _test_type(self, typename, valids, invalids):
        for x in invalids:
            try:
                jsonschema.validate(x, {"disallow":typename})
            except ValueError, e:
                self.fail("Unexpected failure: %s" % e)

        for x in valids:
            self.assertRaises(ValueError, jsonschema.validate, x,
                              {"disallow":typename})

