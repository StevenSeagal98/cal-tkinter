from src.app import main
import unittest

# Function to run the tests
def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__('tests'))
    
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        print("Some tests failed.")
    else:
        print("All tests passed.")

# Run the main function to start the app
if __name__ == '__main__':
    run_tests()
    main()
