import unittest
import parser
import settings
import db

DB = settings.DB(True)

class ParseTest(unittest.TestCase):
    def test_parse(self):
        db.drop_table(DB)
        db.create_index(DB)
        parser.parse("test", True)
        prod = list(DB.products.find())
        self.assertEqual(len(prod), 1)
        self.assertEqual(prod[0]['uid'], '400000022199')


# class ParseCSVTest(unittest.TestCase):
#     def test_parse(self):
#         db.drop_table(DB)
#         db.create_index(DB)
#         parser.parse("csv", True)
#         prod = list(DB.products.find())
#         self.assertEqual(len(prod),  7051)


# class ParseXMLTest(unittest.TestCase):
#     def test_parse(self):
#         db.drop_table(DB)
#         db.create_index(DB)
#         parser.parse("xml", True)
#         prod = list(DB.products.find())
#         self.assertEqual(len(prod),  355)


# Launch tests: python -m unittest tests.py
if __name__ == '__main__':
    unittest.main()