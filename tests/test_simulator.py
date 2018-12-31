import unittest

import simulator 

class TestSimulator(unittest.TestCase):
    
    
    def setUp(self):
        self.sim = simulator.Simulator()


    def test_get_field_val(self):
        cell = simulator.MemoryCell(5)
        cell.bytes = [0, 0, 0, 2, 2]

        self.assertEqual(self.sim.get_field_val(1, 5, cell), 130)


    def test_parse_instruction(self):
        cell = simulator.MemoryCell(5)
        cell.bytes = [8, 2, 5, 6, 1]

        parts = self.sim.parse_instruction(cell)

        self.assertTrue(False)
