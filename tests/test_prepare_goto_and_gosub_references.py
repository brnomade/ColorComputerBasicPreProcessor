import unittest
from color_basic_preprocessor import prepare_goto_and_gosub_references, glb_new_line_symbol, glb_reference_dictionary
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


class TestPrepareGotoAndGosubReferences(unittest.TestCase):

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
        # scenario 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write("_correct:                                                     " + glb_new_line_symbol)
        file_handler.write("01 '                                                            " + glb_new_line_symbol)
        file_handler.write("02 _correct:                                                  " + glb_new_line_symbol)
        file_handler.write("03       _correct:                                            " + glb_new_line_symbol)
        file_handler.write("04 _ incorrect:                                               " + glb_new_line_symbol)
        file_handler.write("05 _this is incorrect                                         " + glb_new_line_symbol)
        file_handler.write("06 _correct:                                                  " + glb_new_line_symbol)
        file_handler.write("07 _correct:                                                  " + glb_new_line_symbol)
        file_handler.write("08 _correct:                                                  " + glb_new_line_symbol)
        file_handler.write("09 _ incorrect label :                                        " + glb_new_line_symbol)
        file_handler.write("10 _incorrect_label                                           " + glb_new_line_symbol)
        file_handler.write("11 _correct_label:                                            " + glb_new_line_symbol)
        file_handler.write("12 _another_incorrect_label                                   " + glb_new_line_symbol)
        file_handler.write("13         _a_very_correct_label:                             " + glb_new_line_symbol)
        file_handler.write("14         _a_very_incorrect_label :                          " + glb_new_line_symbol)
        file_handler.write("15         _ a_very_incorrect_label:                          " + glb_new_line_symbol)
        file_handler.write("16 '         _a_correct_but_irrelevant_label:                 " + glb_new_line_symbol)
        file_handler.write("17 '          an_incorrect_but_irrelevant_label:              " + glb_new_line_symbol)
        file_handler.write("18 '          _another_incorrect_but_irrelevant_label         " + glb_new_line_symbol)
        file_handler.write("19 some code _an_incorrect_scenario                           " + glb_new_line_symbol)
        file_handler.write("20 some code _an_incorrect_scenario:                          " + glb_new_line_symbol)
        file_handler.write("21 some code ' _an_incorrect_scenario_but_irrelevant:         " + glb_new_line_symbol)

        file_handler.close()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, glb_reference_dictionary)
        self.assertEqual(error_codes_list, [12, 10, 13, 13, 10, 10, 10, 13, 11, 11, 13, 13])
        self.assertEqual({'_continue:': '20', '_end:': '50', '_start:': '60', '_closure:': '70', '_correct_label:': '100', '_will_this_work_label:': '120'}, glb_reference_dictionary["gotogosub"])
