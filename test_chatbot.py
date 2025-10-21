import unittest
from chatbot import get_response  # Replace with the actual function name

class TestChatbot(unittest.TestCase):
    def test_valid_input(self):
        # Test case 1: Valid input
        input_data = "What is the shortest route to the city center?"
        expected_output = {"route": "Route A", "distance": "5 km"}  # Replace with actual expected output
        self.assertEqual(get_response(input_data), expected_output)

    def test_invalid_input(self):
        # Test case 2: Invalid input
        input_data = "Blah blah blah"
        expected_output = {"route": None, "distance": None}
        self.assertEqual(get_response(input_data), expected_output)

    def test_empty_input(self):
        # Test case 3: Empty input
        input_data = ""
        expected_output = {"route": None, "distance": None}
        self.assertEqual(get_response(input_data), expected_output)

if __name__ == "__main__":
    unittest.main()