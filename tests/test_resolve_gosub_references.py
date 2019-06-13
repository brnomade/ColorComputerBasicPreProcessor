import unittest
from color_basic_preprocessor import test_resolve_gosub_references, prepare_GOSUB_and_gosub_references
from color_basic_preprocessor import glb_new_line_symbol, glb_reference_dictionary, glb_no_error_code
import os

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
        file_handler.write("10 _scenario_01:                                                  " + glb_new_line_symbol)
        file_handler.write("11                                                                " + glb_new_line_symbol)
        file_handler.write("12 GOSUB _scenario_01:                                            " + glb_new_line_symbol)
        file_handler.write("13 GOSUB           _scenario_01:                                  " + glb_new_line_symbol)
        file_handler.write("14 GOSUB_scenario_01:                                             " + glb_new_line_symbol)
        file_handler.write("15                                                                " + glb_new_line_symbol)
        file_handler.write("16 GOSUB scenario_01:                                             " + glb_new_line_symbol)
        file_handler.write("17 GOSUB           scenario_01:                                   " + glb_new_line_symbol)
        file_handler.write("18 GOSUBscenario_01:                                              " + glb_new_line_symbol)
        file_handler.write("19                                                                " + glb_new_line_symbol)
        file_handler.write("20 GOSUB _scenario_01                                             " + glb_new_line_symbol)
        file_handler.write("21 GOSUB           _scenario_01                                   " + glb_new_line_symbol)
        file_handler.write("22 GOSUB_scenario_01                                              " + glb_new_line_symbol)
        file_handler.write("23                                                                " + glb_new_line_symbol)
        file_handler.write("24 GOSUB scenario_01                                              " + glb_new_line_symbol)
        file_handler.write("25 GOSUB           scenario_01                                    " + glb_new_line_symbol)
        file_handler.write("26 GOSUBscenario_01                                               " + glb_new_line_symbol)
        file_handler.write("27                                                                " + glb_new_line_symbol)
        file_handler.write("28 GOSUB _scenario_01: : GOSUB _scenario_01:                      " + glb_new_line_symbol)
        file_handler.write("29 GOSUB _scenario_01:: commands : GOSUB _scenario_01:            " + glb_new_line_symbol)
        file_handler.write("30 GOSUB _scenario_01:: commands : GOSUB _scenario_02:            " + glb_new_line_symbol)
        file_handler.write("31                                                                " + glb_new_line_symbol)
        file_handler.write("32 _scenario_02:                                                  " + glb_new_line_symbol)
        file_handler.write("33                                                                " + glb_new_line_symbol)
        file_handler.write("34 GOSUB _scenario_22:                                            " + glb_new_line_symbol)
        file_handler.write("35 GOSUB                                                          " + glb_new_line_symbol)
        file_handler.write("36                                                                " + glb_new_line_symbol)
        file_handler.write("37 'GOSUB _scenario_22:                                           " + glb_new_line_symbol)
        file_handler.write("38 GOSUB  _scenario_02: ' GOSUB _scenario_22: GOSUB _scenario_22: " + glb_new_line_symbol)
        file_handler.close()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, glb_reference_dictionary)
        if error_codes_list[0] == glb_no_error_code:
            error_codes_list = test_resolve_gosub_references(glb_input_filename, glb_output_filename, glb_reference_dictionary)
            print(error_codes_list)
            self.assertEqual(error_codes_list, [23, 23, 23, 21, 21, 21, 21, 21, 21, 20, 20, 22, 21])
        else:
            self.fail("error on pre-condition method.")
