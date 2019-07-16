import unittest
from color_basic_preprocessor import prepare_goto_and_gosub_references, initialise_a_reference_dictionary
from color_basic_preprocessor import glb_new_line_symbol, glb_error_gotogosub_duplicate_reference
import os

glb_input_filename = "in_prepare_goto_and_gosub_references.txt"
glb_output_filename = "out_prepare_goto_and_gosub_references.txt"
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


class TestPrepareGotoAndGosubReferences(unittest.TestCase):

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
        # scenario 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write(glb_new_line_symbol)
        file_handler.write("                                                         " + glb_new_line_symbol)
        file_handler.write("some code not related                                    " + glb_new_line_symbol)
        file_handler.write("_invalid_reference :                                     " + glb_new_line_symbol)
        file_handler.write("_invalid_reference :                                     " + glb_new_line_symbol)
        file_handler.write("_invalid_reference                                       " + glb_new_line_symbol)
        file_handler.write("       _invalid_reference :                              " + glb_new_line_symbol)
        file_handler.write("_ invalid_reference:                                     " + glb_new_line_symbol)
        file_handler.write("   _ invalid_reference:                                  " + glb_new_line_symbol)
        file_handler.write("   _     invalid_reference:                              " + glb_new_line_symbol)
        file_handler.write("    _ invalid_reference :                                " + glb_new_line_symbol)
        file_handler.write("    invalid_reference                                    " + glb_new_line_symbol)
        file_handler.write("invalid_reference:                                       " + glb_new_line_symbol)
        file_handler.write("invalid_reference :                                      " + glb_new_line_symbol)
        file_handler.write("'_irrelevant:                                            " + glb_new_line_symbol)
        file_handler.write("'_irrelevant:                                            " + glb_new_line_symbol)
        file_handler.write("' _irrelevant                                            " + glb_new_line_symbol)
        file_handler.write("      _correct:                                          " + glb_new_line_symbol)
        file_handler.write("_correct1:                                               " + glb_new_line_symbol)
        file_handler.write("_correct2:'some comment                                  " + glb_new_line_symbol)
        file_handler.write("_correct3: 'some comment                                 " + glb_new_line_symbol)
        file_handler.write("_correct4: some code                                     " + glb_new_line_symbol)
        file_handler.write("_correct5:       some code                               " + glb_new_line_symbol)
        file_handler.write("_correct5:       some code  'duplicate                   " + glb_new_line_symbol)
        file_handler.write("some code: _invalid_reference:                           " + glb_new_line_symbol)
        file_handler.write("some code:       _invalid_reference:                     " + glb_new_line_symbol)
        file_handler.close()
        a_reference_dictionary = initialise_a_reference_dictionary()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
        self.assertEqual(a_reference_dictionary["gotogosub"],
                         {'_correct:': {'file_line': '18'}, '_correct1:': {'file_line': '19'},
                          '_correct2:': {'file_line': '20'}, '_correct3:': {'file_line': '21'},
                          '_correct4:': {'file_line': '22'}, '_correct5:': {'file_line': '23'}})
        self.assertEqual(error_codes_list, [10])

    def test_scenario_2(self):
        # scenario 1 - duplicated reference name
        file_handler = open(glb_input_filename, "w")
        file_handler.write("_correct1:                                               " + glb_new_line_symbol)
        file_handler.write("some code                                                " + glb_new_line_symbol)
        file_handler.write("_correct1:                                               " + glb_new_line_symbol)
        file_handler.write("some code                                                " + glb_new_line_symbol)
        file_handler.close()
        a_reference_dictionary = initialise_a_reference_dictionary()
        error_codes_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_reference_dictionary)
        self.assertEqual(a_reference_dictionary["gotogosub"],
                         {'_correct1:': {'file_line': "3"}})
        self.assertEqual(error_codes_list, [glb_error_gotogosub_duplicate_reference])


if __name__ == '__main__':
    unittest.main()
