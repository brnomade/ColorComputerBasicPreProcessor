import unittest
from color_basic_preprocessor import resolve_goto_references, prepare_goto_and_gosub_references
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
        file_handler.write("10 _scenario_01:                                          " + glb_new_line_symbol)
        file_handler.write("11                                                        " + glb_new_line_symbol)
        file_handler.write("12 GOTO _scenario_01:                                     " + glb_new_line_symbol)
        file_handler.write("13 GOTO           _scenario_01:                           " + glb_new_line_symbol)
        file_handler.write("14 GOTO_scenario_01:                                      " + glb_new_line_symbol)
        file_handler.write("15                                                        " + glb_new_line_symbol)
        file_handler.write("16 GOTO scenario_01:                                      " + glb_new_line_symbol)
        file_handler.write("17 GOTO           scenario_01:                            " + glb_new_line_symbol)
        file_handler.write("18 GOTOscenario_01:                                       " + glb_new_line_symbol)
        file_handler.write("19                                                        " + glb_new_line_symbol)
        file_handler.write("20 GOTO _scenario_01                                      " + glb_new_line_symbol)
        file_handler.write("21 GOTO           _scenario_01                            " + glb_new_line_symbol)
        file_handler.write("22 GOTO_scenario_01                                       " + glb_new_line_symbol)
        file_handler.write("23                                                        " + glb_new_line_symbol)
        file_handler.write("24 GOTO scenario_01                                       " + glb_new_line_symbol)
        file_handler.write("25 GOTO           scenario_01                             " + glb_new_line_symbol)
        file_handler.write("26 GOTOscenario_01                                        " + glb_new_line_symbol)
        file_handler.write("27                                                        " + glb_new_line_symbol)
        file_handler.write("28 GOTO _scenario_01: : GOTO _scenario_01:                " + glb_new_line_symbol)
        file_handler.write("28 GOTO _scenario_01:: commands : GOTO _scenario_01:      " + glb_new_line_symbol)
        file_handler.write("29                                                        " + glb_new_line_symbol)
        file_handler.write("30 _scenario_02:                                          " + glb_new_line_symbol)
        file_handler.write("31                                                        " + glb_new_line_symbol)
        file_handler.write("32 GOTO _scenario_22:                                     " + glb_new_line_symbol)
        file_handler.write("33 GOTO                                                   " + glb_new_line_symbol)
        file_handler.write("34                                                        " + glb_new_line_symbol)
        file_handler.write("35 'GOTO _scenario_22:                                    " + glb_new_line_symbol)
        file_handler.write("36 GOTO  _scenario_02: ' GOTO _scenario_22: _scenario_22:  " + glb_new_line_symbol)
        file_handler.close()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, glb_reference_dictionary)
        if error_codes_list[0] == glb_no_error_code:
            error_codes_list = resolve_goto_references(glb_input_filename, glb_output_filename, glb_reference_dictionary)
            print(error_codes_list)
            self.assertEqual(error_codes_list, [23, 23, 23, 21, 21, 21, 21, 21, 21, 20, 20, 22, 21])
        else:
            self.fail("error on pre-condition method.")
