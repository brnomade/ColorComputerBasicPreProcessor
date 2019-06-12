import unittest
from color_basic_preprocessor import add_line_numbers, glb_space_symbol, glb_line_number_increment, glb_line_number_start
import os

glb_new_line_symbol = "\n"
glb_input_filename = "unit_test_input.txt"
glb_output_filename = "unit_test_output.txt"


def count_number_of_lines_in_file(a_file_name):
    counter = 0
    with open(a_file_name, "r") as file_handler:
        for a_line in file_handler:
            counter = counter + 1
    return counter


def print_file(a_file_name):
    print("File:", a_file_name)
    print("BEGIN[")
    with open(a_file_name, "r") as file_handler:
        for a_line in file_handler:
            print(a_line)
    print("]END")


class TestAddLineNumbers(unittest.TestCase):

    def setUp(self):
        print(' ', type(self).__name__, '- setUp - nothing to setup')

    def tearDown(self):
        if os.path.exists(glb_input_filename):
            os.remove(glb_input_filename)
        else:
            print("can't find file", glb_input_filename, ". will not delete it.")
        if os.path.exists(glb_output_filename):
            os.remove(glb_output_filename)
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")

    def test_scenario_1(self):
        # scenario 1 - file contains a variety of lines
        file_handler = open(glb_input_filename, "w")
        file_handler.write("'" + glb_new_line_symbol)
        file_handler.write(" " + glb_new_line_symbol)
        file_handler.write("" + glb_new_line_symbol)
        file_handler.write(" yada yada yada " + glb_new_line_symbol)
        file_handler.write(" YADA YADA YADA " + glb_new_line_symbol)
        file_handler.write("yada yada yada " + glb_new_line_symbol)
        file_handler.write("YADA YADA YADA " + glb_new_line_symbol)
        file_handler.write(" yada yada yada" + glb_new_line_symbol)
        file_handler.write(" YADA YADA YADA" + glb_new_line_symbol)
        file_handler.write("yada yada yada" + glb_new_line_symbol)
        file_handler.write("YADA YADA YADA" + glb_new_line_symbol)
        file_handler.close()
        error_codes_list = add_line_numbers(glb_input_filename, glb_output_filename)
        if error_codes_list[0] == 0:
            with open(glb_output_filename, "r") as file_handler:
                line_counter = 0
                for a_line in file_handler:
                    if not a_line.split(glb_space_symbol)[0] == str(glb_line_number_start + (line_counter * glb_line_number_increment)):
                        self.assertTrue(False)
                    line_counter = line_counter + 1
        self.assertTrue(True)

    def test_scenario_2(self):
        # scenario 2 - file is totally empty
        file_handler = open(glb_input_filename, "w")
        file_handler.write("")
        file_handler.close()
        error_codes_list = add_line_numbers(glb_input_filename, glb_output_filename)
        if error_codes_list[0] == 0:
            with open(glb_output_filename, "r") as file_handler:
                line_counter = 0
                for a_line in file_handler:
                    if not a_line.split(glb_space_symbol)[0] == str(glb_line_number_start + (line_counter * glb_line_number_increment)):
                        self.assertTrue(False)
                    line_counter = line_counter + 1
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
