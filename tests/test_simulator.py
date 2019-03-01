import unittest

from simulator import Simulator, Sign, Word, Register

class TestSimulator(unittest.TestCase):
    
    
    def setUp(self):
        self.sim = Simulator()


    def test_get_next_instruction(self):
        self.assertEqual(self.sim.get_next_instruction().value, 0)
        self.assertEqual(self.sim.rP.value, 1)


    def test_get_field_val(self):
        cell = Word()
        cell.value = 130

        self.assertEqual(self.sim.get_field_val(1, 5, cell), 130)
        self.assertEqual(self.sim.get_field_val(1, 4, cell), 2)

        cell.value = 134762881

        self.assertEqual(self.sim.get_field_val(1, 1, cell), 8)
        self.assertEqual(self.sim.get_field_val(2, 2, cell), 2)
        self.assertEqual(self.sim.get_field_val(3, 3, cell), 5)
        self.assertEqual(self.sim.get_field_val(4, 4, cell), 6)
        self.assertEqual(self.sim.get_field_val(5, 5, cell), 1)


    def test_LD(self):
        self.sim.memory[43] = Word(300)
        self.sim.memory[86] = Word(-30)

        test_register = Register()

        self.sim.LD(test_register, 43, (0, 5))
        self.assertEqual(test_register.value, 300)
        self.assertEqual(test_register.sign, Sign.POS)

        self.sim.LD(test_register, 86, (0, 5))
        self.assertEqual(test_register.value, 30)
        self.assertEqual(test_register.sign, Sign.NEG)


    def test_LDN(self):
        self.sim.memory[75] = Word(56)
        self.sim.memory[92] = Word(-4000)

        test_register = Register()

        self.sim.LDN(test_register, 75, (0, 5))
        self.assertEqual(test_register.value, 56)
        self.assertEqual(test_register.sign, Sign.NEG)

        self.sim.LDN(test_register, 92, (0, 5))
        self.assertEqual(test_register.value, 4000)
        self.assertEqual(test_register.sign, Sign.POS)


    def test_ADD(self):
        self.sim.memory[10] = Word(400)
        self.sim.memory[11] = Word(532)
        self.sim.memory[12] = Word(-932)
        self.sim.memory[13] = Word(-20)

        self.sim.ADD(10, (0, 5))
        self.assertEqual(self.sim.rA.value, 400)
        self.assertEqual(self.sim.rA.sign, Sign.POS)

        self.sim.ADD(11, (0, 5))
        self.assertEqual(self.sim.rA.value, 932)
        self.assertEqual(self.sim.rA.sign, Sign.POS)

        self.sim.ADD(12, (0, 5))
        self.assertEqual(self.sim.rA.value, 0)
        self.assertEqual(self.sim.rA.sign, Sign.POS)

        self.sim.ADD(13, (0, 5))
        self.assertEqual(self.sim.rA.value, 20)
        self.assertEqual(self.sim.rA.sign, Sign.NEG)


    def test_parse_instruction(self):
        cell = Word()
        #parts = self.sim.parse_instruction(cell)
        self.assertTrue(False)


    def test_instruction_dispatch(self):
        self.assertTrue(False)
