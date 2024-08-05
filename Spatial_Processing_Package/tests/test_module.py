#%%
import unittest
from package.Z_Important_functions import hello

class TestImp_func(unittest.TestCase):
    def test_example(self):
        self.assertEqual(hello(),"Hello from Imp_func!")

# If this script is being run directly, not imported
if __name__ == "__main__":
    unittest.main()  # Run all the test cases in this module