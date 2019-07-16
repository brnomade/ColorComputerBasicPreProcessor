import unittest
from color_basic_preprocessor import initialise_a_reference_dictionary, initialise_available_numeric_references_list, initialise_available_string_references_list
from color_basic_preprocessor import process_procedure_declaration, prepare_variables_references, prepare_goto_and_gosub_references
from color_basic_preprocessor import glb_new_line_symbol, glb_error_declare_duplicate_identifier, glb_no_error_code
import os

glb_input_filename = "in_identifier_uniqueness.txt"
glb_output_filename = "out_identifier_uniqueness.txt"
param_remove_file_after_test = True


class TestIdentifierUniqueness(unittest.TestCase):

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
        # DECLARE identifier is defined first
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE _x():                                                       " + glb_new_line_symbol)
        file_handler.write("LET _x:                                                             " + glb_new_line_symbol)
        file_handler.write("_x:                                                                 " + glb_new_line_symbol)
        file_handler.close()
        #
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        #
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [glb_no_error_code])
        self.assertEqual({'_x': {'line': 2, 'parameters': []}}, a_dictionary["declares"])
        #
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [glb_error_declare_duplicate_identifier])
        self.assertEqual({}, a_dictionary["variables"])
        #
        an_error_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [glb_error_declare_duplicate_identifier])
        self.assertEqual({}, a_dictionary["gotogosub"])


    def test_scenario_2(self):
        # variable identifier is defined first
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET _x:                                                             " + glb_new_line_symbol)
        file_handler.write("DECLARE _x():                                                       " + glb_new_line_symbol)
        file_handler.write("_x:                                                                 " + glb_new_line_symbol)
        file_handler.close()
        #
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        #
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [glb_no_error_code])
        self.assertEqual({'_x': 'AA'}, a_dictionary["variables"])
        #
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [glb_error_declare_duplicate_identifier])
        self.assertEqual({}, a_dictionary["declares"])
        #
        an_error_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [glb_error_declare_duplicate_identifier])
        self.assertEqual({}, a_dictionary["gotogosub"])

    def test_scenario_3(self):
        # goto/gosub reference identifier is defined first
        file_handler = open(glb_input_filename, "w")
        file_handler.write("_x:                                                                 " + glb_new_line_symbol)
        file_handler.write("LET _x:                                                             " + glb_new_line_symbol)
        file_handler.write("DECLARE _x():                                                       " + glb_new_line_symbol)
        file_handler.close()
        #
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references_list = initialise_available_numeric_references_list()
        an_available_string_references_list = initialise_available_string_references_list()
        #
        an_error_list = prepare_goto_and_gosub_references(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [glb_no_error_code])
        self.assertEqual({'_x': {'file_line': '1'}}, a_dictionary["gotogosub"])
        #
        an_error_list = prepare_variables_references(glb_input_filename, glb_output_filename, a_dictionary, an_available_numeric_references_list, an_available_string_references_list)
        self.assertEqual(an_error_list, [glb_error_declare_duplicate_identifier])
        self.assertEqual({}, a_dictionary["variables"])
        #
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [glb_error_declare_duplicate_identifier])
        self.assertEqual({}, a_dictionary["declares"])
        #

if __name__ == '__main__':
    unittest.main()
