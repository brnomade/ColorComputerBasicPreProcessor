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
            # os.remove(glb_input_filename)
            print("D")
        else:
            print("can't find file", glb_input_filename, ". will not delete it.")
        if os.path.exists(glb_output_filename):
            # os.remove(glb_output_filename)
            print("D")
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")

    def test_scenario_1(self):
        # scenario 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write("10 _location_01:                                                " + glb_new_line_symbol)
        file_handler.write("11                                                              " + glb_new_line_symbol)
        file_handler.write("12 GOTO _location_01:                                           " + glb_new_line_symbol)
        file_handler.write("13 GOTO           _location_01:                                 " + glb_new_line_symbol)
        file_handler.write("14 GOTO_location_01:                                            " + glb_new_line_symbol)
        file_handler.write("15                                                              " + glb_new_line_symbol)
        file_handler.write("16 some code : GOTO _location_01:                               " + glb_new_line_symbol)
        file_handler.write("17 some code: GOTO           _location_01:                      " + glb_new_line_symbol)
        file_handler.write("18 some code:GOTO_location_01:                                  " + glb_new_line_symbol)
        file_handler.write("19 some code :GOTO_location_01:: some code                      " + glb_new_line_symbol)
        file_handler.write("20                                                              " + glb_new_line_symbol)
        file_handler.write("21 GOTO location_01:                                            " + glb_new_line_symbol)
        file_handler.write("22 GOTO           location_01:                                  " + glb_new_line_symbol)
        file_handler.write("23 GOTOlocation_01:                                             " + glb_new_line_symbol)
        file_handler.write("24                                                              " + glb_new_line_symbol)
        file_handler.write("25 GOTO _location_01                                            " + glb_new_line_symbol)
        file_handler.write("26 GOTO           _location_01                                  " + glb_new_line_symbol)
        file_handler.write("27 GOTO_location_01                                             " + glb_new_line_symbol)
        file_handler.write("28                                                              " + glb_new_line_symbol)
        file_handler.write("29 GOTO location_01                                             " + glb_new_line_symbol)
        file_handler.write("30 GOTO           location_01                                   " + glb_new_line_symbol)
        file_handler.write("31 GOTOlocation_01                                              " + glb_new_line_symbol)
        file_handler.write("32                                                              " + glb_new_line_symbol)
        file_handler.write("33 GOTO _location_01: : GOTO _location_01:                      " + glb_new_line_symbol)
        file_handler.write("34 GOTO _location_01:: commands : GOTO _location_01:            " + glb_new_line_symbol)
        file_handler.write("35                                                              " + glb_new_line_symbol)
        file_handler.write("36 _location_02:                                                " + glb_new_line_symbol)
        file_handler.write("37                                                              " + glb_new_line_symbol)
        file_handler.write("38 GOTO _location_22:                                           " + glb_new_line_symbol)
        file_handler.write("39 GOTO                                                         " + glb_new_line_symbol)
        file_handler.write("40                                                              " + glb_new_line_symbol)
        file_handler.write("41 'GOTO _location_22:                                          " + glb_new_line_symbol)
        file_handler.write("42 GOTO  _location_02: ' GOTO _location_22: GOTO _location_22:  " + glb_new_line_symbol)
        file_handler.close()
        a_reference_dictionary = initialise_a_reference_dictionary()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
        if error_codes_list[0] == glb_no_error_code:
            error_codes_list = resolve_goto_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
            print(error_codes_list)
            self.assertEqual(error_codes_list, [23, 23, 23, 21, 21, 21, 21, 21, 21, 20, 20, 22, 21])
        else:
            self.fail("error on pre-condition method.")


if __name__ == '__main__':
    unittest.main()
