import unittest
from color_basic_preprocessor import resolve_goto_references, prepare_goto_and_gosub_references, initialise_a_reference_dictionary
from color_basic_preprocessor import glb_new_line_symbol, glb_no_error_code
import os

glb_input_filename = "in_resolve_goto_references.txt"
glb_output_filename = "out_resolve_goto_references.txt"


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


class TestResolveGotoReferencesTest(unittest.TestCase):

    def setUp(self):
        print(' ', type(self).__name__, '- setUp - nothing to setup')

    def tearDown(self):
        if os.path.exists(glb_input_filename):
            os.remove(glb_input_filename)
            # print("D")
        else:
            print("can't find file", glb_input_filename, ". will not delete it.")
        if os.path.exists(glb_output_filename):
            os.remove(glb_output_filename)
            # print("D")
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")

    def test_scenario_1(self):
        # scenario 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write(glb_new_line_symbol)
        file_handler.write("PRINT:PRINT:PRINT:                                           " + glb_new_line_symbol)
        file_handler.write("_location_01:                                                " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOTO _location_01:                                           " + glb_new_line_symbol)
        file_handler.write("GOTO           _location_01:                                 " + glb_new_line_symbol)
        file_handler.write("GOTO_location_01:                                            " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("some code : GOTO _location_01:                               " + glb_new_line_symbol)
        file_handler.write("some code: GOTO           _location_01:                      " + glb_new_line_symbol)
        file_handler.write("some code:GOTO_location_01:                                  " + glb_new_line_symbol)
        file_handler.write("some code:GOTO _location_01:                                  " + glb_new_line_symbol)
        file_handler.write("some code :GOTO_location_01:: some code                      " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOTO location_01:                                            " + glb_new_line_symbol)
        file_handler.write("GOTO           location_01:                                  " + glb_new_line_symbol)
        file_handler.write("GOTOlocation_01:                                             " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOTO _location_01                                            " + glb_new_line_symbol)
        file_handler.write("GOTO           _location_01                                  " + glb_new_line_symbol)
        file_handler.write("GOTO_location_01                                             " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOTO location_01                                             " + glb_new_line_symbol)
        file_handler.write("GOTO           location_01                                   " + glb_new_line_symbol)
        file_handler.write("GOTOlocation_01                                              " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOTO _location_01: : GOTO _location_01:                      " + glb_new_line_symbol)
        file_handler.write("GOTO _location_01:: commands : GOTO _location_01:            " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("_location_02:                                                " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOTO _location_22:                                           " + glb_new_line_symbol)
        file_handler.write("GOTO                                                         " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("'GOTO _location_22:                                          " + glb_new_line_symbol)
        file_handler.write("GOTO  _location_02: ' GOTO _location_22: GOTO _location_22:  " + glb_new_line_symbol)
        file_handler.write("GOTO  _location_02:GOTO _location_22:'GOTO _location_22:  " + glb_new_line_symbol)
        file_handler.close()
        a_reference_dictionary = initialise_a_reference_dictionary()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
        print(a_reference_dictionary)
        if error_codes_list[0] == glb_no_error_code:
            error_codes_list = resolve_goto_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
            self.assertEqual(error_codes_list, [20, 20, 22, 20])
        else:
            self.fail("error on pre-condition method.")


if __name__ == '__main__':
    unittest.main()
