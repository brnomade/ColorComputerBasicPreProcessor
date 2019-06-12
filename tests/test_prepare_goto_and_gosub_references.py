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

    def test_scenario_1( self ):
        # scenario 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write("_continue:                          " + glb_new_line_symbol)
        file_handler.write("10 _continue:                          " + glb_new_line_symbol)
        file_handler.write("20 _continue:                          " + glb_new_line_symbol)
        file_handler.write("30 _ continue:                         " + glb_new_line_symbol)
        file_handler.write("40 _this is a wrong label              " + glb_new_line_symbol)
        file_handler.write("50 _end:                               " + glb_new_line_symbol)
        file_handler.write("60 _start:                             " + glb_new_line_symbol)
        file_handler.write("70 _closure:                           " + glb_new_line_symbol)
        file_handler.write("80 _ incorrect label :                 " + glb_new_line_symbol)
        file_handler.write("90 _incorrect_label                    " + glb_new_line_symbol)
        file_handler.write("100 _correct_label:                     " + glb_new_line_symbol)
        file_handler.write("110 _another_incorrect_label            " + glb_new_line_symbol)
        file_handler.write("120         _will_this_work_label:      " + glb_new_line_symbol)
        file_handler.write("130         _will_this_work_label :     " + glb_new_line_symbol)
        file_handler.write("140         _ will_this_work_label:     " + glb_new_line_symbol)
        file_handler.close()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, glb_reference_dictionary)
        self.assertEqual(error_codes_list, [12, 10, 13, 13, 13, 11, 11, 13, 13])
        self.assertEqual({'_continue:': '20', '_end:': '50', '_start:': '60', '_closure:': '70', '_correct_label:': '100', '_will_this_work_label:': '120'}, glb_reference_dictionary["gotogosub"])

