import unittest

from fun.trading.futures_contract_specs import FuturesContractSpecs


class TestFuturesSpecs(unittest.TestCase):
    def test_lookup_contract_unit(self):
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("es"), 50)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("ym"), 5)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("rty"), 50)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("nyd"), 5)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("nq"), 20)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zb"), 1000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zn"), 1000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zf"), 1000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zt"), 1000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("ge"), 2500)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6e"), 125000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6j"), 12500000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6a"), 100000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6b"), 62500)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6c"), 100000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6s"), 125000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6n"), 100000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("6m"), 500000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("gc"), 100)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("si"), 5000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("hg"), 25000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("pl"), 50)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("cl"), 1000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("rb"), 42000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("ng"), 10000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("ho"), 42000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zs"), 5000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zc"), 5000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zw"), 5000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zl"), 60000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("zm"), 100)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("le"), 40000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("he"), 40000)
        self.assertEqual(FuturesContractSpecs.lookup_contract_unit("gf"), 50000)


if __name__ == "__main__":
    unittest.main()
