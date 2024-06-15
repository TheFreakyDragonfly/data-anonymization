import unittest
from anonymizer import config_from_cs


class TestAnonymizer(unittest.TestCase):
    def test_cs_to_config(self):
        # self.assertEqual(True, False)  # add assertion here
        print(config_from_cs('Server=tcp:sqls-dataanon-dev-001.database.windows.net,1433;Initial Catalog=Northwind;Persist Security Info=False;User ID=data-anon;Password=Lantanio13891!;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'))


if __name__ == '__main__':
    unittest.main()
