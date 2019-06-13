import unittest
from color_basic_preprocessor import prepare_goto_and_gosub_references, initialise_a_reference_dictionary
from color_basic_preprocessor import glb_new_line_symbol
import os

glb_input_filename = "in_prepare_goto_and_gosub_references.txt"
glb_output_filename = "out_prepare_goto_and_gosub_references.txt"


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
        file_handler.write(glb_new_line_symbol)
        file_handler.write("_missing_line_number:                                         " + glb_new_line_symbol)
        file_handler.write("AA _strings_instead_of_line_number_at_start_of_line:          " + glb_new_line_symbol)
        file_handler.write("10 '_irrelevant:                                              " + glb_new_line_symbol)
        file_handler.write("11 ' _also_irrelevant                                         " + glb_new_line_symbol)
        file_handler.write("12_incorrect:                                                 " + glb_new_line_symbol)
        file_handler.write("13       _correct1:                                           " + glb_new_line_symbol)
        file_handler.write("14 _ incorrect:                                               " + glb_new_line_symbol)
        file_handler.write("15 _this_is_incorrect                                         " + glb_new_line_symbol)
        file_handler.write("16 _correct2:                                                 " + glb_new_line_symbol)
        file_handler.write("17 _correct2:                                                 " + glb_new_line_symbol)
        file_handler.write("18 _correct:                                                  " + glb_new_line_symbol)
        file_handler.write("19 _ incorrect label :                                        " + glb_new_line_symbol)
        file_handler.write("20 _incorrect_label                                           " + glb_new_line_symbol)
        file_handler.write("21 _correct_label:                                            " + glb_new_line_symbol)
        file_handler.write("22 _another_incorrect_label                                   " + glb_new_line_symbol)
        file_handler.write("23        _a_very_correct_label:                              " + glb_new_line_symbol)
        file_handler.write("24        _a_very_incorrect_label :                           " + glb_new_line_symbol)
        file_handler.write("25        _ a_very_incorrect_label:                           " + glb_new_line_symbol)
        file_handler.write("26 '         _a_correct_but_irrelevant_label:                 " + glb_new_line_symbol)
        file_handler.write("'27          an_incorrect_but_irrelevant_label:               " + glb_new_line_symbol)
        file_handler.write("28 '          _another_incorrect_but_irrelevant_label         " + glb_new_line_symbol)
        file_handler.write("29 some code _an_incorrect_scenario                           " + glb_new_line_symbol)
        file_handler.write("30 some code _an_incorrect_scenario:                          " + glb_new_line_symbol)
        file_handler.write("31 _an_invalid_reference: some code following it              " + glb_new_line_symbol)
        file_handler.close()
        a_reference_dictionary = initialise_a_reference_dictionary()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
        self.assertEqual(error_codes_list, [12, 12, 12, 13, 11, 10, 13, 11, 11, 13, 13, 12, 13])
        self.assertEqual({'_correct1:': '13', '_correct2:': '16', '_correct:': '18', '_correct_label:': '21', '_a_very_correct_label:': '23'}, a_reference_dictionary["gotogosub"])


if __name__ == '__main__':
    unittest.main()
