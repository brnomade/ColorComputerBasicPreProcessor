import unittest
from color_basic_preprocessor import initialise_a_reference_dictionary, initialise_available_numeric_references_list, initialise_available_string_references_list, prepare_variables_references
from color_basic_preprocessor import glb_new_line_symbol
import os

glb_input_filename = "in_prepare_variables_references.txt"
glb_output_filename = "out_prepare_variables_references.txt"
param_remove_file_after_test = True


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


class TestPrepareVariablesReferences(unittest.TestCase):

    def setUp(self):
        print(' ', type(self).__name__, '- setUp - nothing to setup')

    def tearDown(self):
        if os.path.exists(glb_input_filename):
            if param_remove_file_after_test:
                os.remove(glb_input_filename)
        else:
            print("can't find file", glb_input_filename, ". will not delete it.")
        if os.path.exists(glb_output_filename):
            if param_remove_file_after_test:
                os.remove(glb_output_filename)
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")

    def test_scenario_1(self):
        # file is empty, file has empty lines, file has lines with only spaces, file has no variables defined
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        file_handler = open(glb_input_filename, "w")
        file_handler.write("")
        file_handler.write(glb_new_line_symbol)
        file_handler.write("                                                                                          " + glb_new_line_symbol)
        file_handler.write("some code: some code: some code: some code                                                " + glb_new_line_symbol)
        file_handler.write("some code: 'some code: some code: some code : LET x:                                      " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [0])
        self.assertEqual({}, a_dictionary["variables"])

    def test_scenario_2(self):
        # not valid variables declarations
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET                                                                                       " + glb_new_line_symbol)
        file_handler.write("LET : LET : LET : LET                                                                     " + glb_new_line_symbol)
        file_handler.write("LET x  =                                                                                  " + glb_new_line_symbol)
        file_handler.write("LET 0  =                                                                                  " + glb_new_line_symbol)
        file_handler.write("LET (  =                                                                                  " + glb_new_line_symbol)
        file_handler.write("LET x                                                                                     " + glb_new_line_symbol)
        file_handler.write("LET x$                                                                                    " + glb_new_line_symbol)
        file_handler.write("LET x + y                                                                                 " + glb_new_line_symbol)
        file_handler.write("LET x, y, z: LET x y z: LET z                                                             " + glb_new_line_symbol)
        file_handler.write("LET x, :                                                                                  " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [42, 42, 42, 42, 42, 42, 42, 42, 42, 42])
        self.assertEqual({}, a_dictionary["variables"])

    def test_scenario_3(self):
        # invalid variables names
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET 0: LET 10: LET 200: LET 012345:                                                       " + glb_new_line_symbol)
        file_handler.write("LET 0$ : LET 10$ : LET 200$ : LET 012345$:                                                " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [46, 46, 46, 46, 46, 46, 46, 46])
        self.assertEqual({}, a_dictionary["variables"])

    def test_scenario_4(self):
        # uniqueness
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET x: LET x:                                                                             " + glb_new_line_symbol)
        file_handler.write("LET x$ : LET x$:                                                                          " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [45, 45])
        self.assertEqual({'x': 'AA', 'x$': 'AA$'}, a_dictionary["variables"])

    def test_scenario_5(self):
        # number of variables exceeded
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        an_available_numeric_references_list.clear()
        an_available_string_references_list.clear()
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET y:                                                                                    " + glb_new_line_symbol)
        file_handler.write("LET y$:                                                                                   " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [44, 43])
        self.assertEqual({}, a_dictionary["variables"])

    def test_scenario_6(self):
        # all valid
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET x: LET y: LET z: LET w :                                                              " + glb_new_line_symbol)
        file_handler.write("LET x$ : LET y$: LET z$ : LET w$:                                                         " + glb_new_line_symbol)
        file_handler.write("LET a_very_long_name_with_0123 : LET a_very_long_name_with_0123$:                         " + glb_new_line_symbol)
        file_handler.write(" some code : some code : some code : LET abc :                                            " + glb_new_line_symbol)
        file_handler.write("LET _a_valid_name: LET _a_valid_name$:                                                    " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [0])
        self.assertEqual({'x': 'AA', 'y': 'AB', 'z': 'AC', 'w': 'AD',
                          'x$': 'AA$', 'y$': 'AB$', 'z$': 'AC$', 'w$': 'AD$',
                          'a_very_long_name_with_0123': 'AE', 'a_very_long_name_with_0123$': 'AE$',
                          'abc': 'AF',
                          '_a_valid_name': 'AG', '_a_valid_name$': 'AF$'},
                         a_dictionary["variables"])


if __name__ == '__main__':
    unittest.main()
