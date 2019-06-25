import unittest
from color_basic_preprocessor import prepare_goto_and_gosub_references, resolve_gosub_references, initialise_a_reference_dictionary
from color_basic_preprocessor import glb_new_line_symbol, glb_no_error_code
import os

glb_input_filename = "in_resolve_gosub_references.txt"
glb_output_filename = "out_resolve_gosub_references.txt"


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


class TestResolveGosubReferences(unittest.TestCase):

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
        file_handler.write("_location_01:                                                 " + glb_new_line_symbol)
        file_handler.write("                                                             " + glb_new_line_symbol)
        file_handler.write("GOSUB _location_01:                                           " + glb_new_line_symbol)
        file_handler.write("GOSUB           _location_01:                                 " + glb_new_line_symbol)
        file_handler.write("GOSUB_location_01:                                            " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("some code : GOSUB _location_01:                               " + glb_new_line_symbol)
        file_handler.write("some code: GOSUB           _location_01:                      " + glb_new_line_symbol)
        file_handler.write("some code:GOSUB_location_01:                                  " + glb_new_line_symbol)
        file_handler.write("some code:GOSUB _location_01:                                  " + glb_new_line_symbol)
        file_handler.write("some code :GOSUB_location_01:                                 " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("GOSUB location_01:                                            " + glb_new_line_symbol)
        file_handler.write("GOSUB           location_01:                                  " + glb_new_line_symbol)
        file_handler.write("GOSUBlocation_01:                                             " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("GOSUB _location_01                                            " + glb_new_line_symbol)
        file_handler.write("GOSUB           _location_01                                  " + glb_new_line_symbol)
        file_handler.write("GOSUB_location_01                                             " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("GOSUB location_01                                             " + glb_new_line_symbol)
        file_handler.write("GOSUB           location_01                                   " + glb_new_line_symbol)
        file_handler.write("GOSUBlocation_01                                              " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("GOSUB _location_01: : GOSUB _location_01:                     " + glb_new_line_symbol)
        file_handler.write("GOSUB _location_01:: commands : GOSUB _location_01:           " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("_location_02:                                                 " + glb_new_line_symbol)
        file_handler.write("_location_22:                                                 " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("GOSUB _location_23:                                           " + glb_new_line_symbol)
        file_handler.write("GOSUB                                                         " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("'GOSUB _location_22:                                          " + glb_new_line_symbol)
        file_handler.write("GOSUB  _location_02: ' GOSUB _location_22: GOSUB _location_30:" + glb_new_line_symbol)
        file_handler.write("GOSUB  _location_02:GOSUB _location_22: '  GOSUB _location_30:" + glb_new_line_symbol)
        file_handler.write("commands : GOSUB  _location_02: commands ' GOSUB _location_22:" + glb_new_line_symbol)
        file_handler.write("commands : GOSUB  _location_02: commands :GOSUB _location_22: " + glb_new_line_symbol)
        file_handler.write("                                                              " + glb_new_line_symbol)
        file_handler.write("GOSUB_location_02::GOSUB_location_22::GOSUB _location_30:     " + glb_new_line_symbol)
        file_handler.close()
        a_reference_dictionary = initialise_a_reference_dictionary()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
        if error_codes_list[0] == glb_no_error_code:
            error_codes_list = resolve_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
            self.assertEqual(error_codes_list, [31, 31])
        else:
            self.fail("error on pre-condition method.")


if __name__ == '__main__':
    unittest.main()
