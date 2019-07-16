import unittest
from color_basic_preprocessor import process_procedure_declaration, initialise_a_reference_dictionary
from color_basic_preprocessor import glb_new_line_symbol
import os

glb_input_filename = "in_process_procedure_declaration.txt"
glb_output_filename = "out_process_procedure_declaration.txt"
param_remove_file_after_test = True

class TestProcessProcedureDeclaration(unittest.TestCase):

    def setUp(self):
        file_handler = open(glb_input_filename, "w")
        file_handler.write("")
        file_handler.close()

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
        # file is empty, file has empty lines, file has lines with only spaces, file has no procedures declared
        file_handler = open(glb_input_filename, "w")
        file_handler.write("")
        file_handler.write(glb_new_line_symbol)
        file_handler.write("                                                                                          " + glb_new_line_symbol)
        file_handler.write("some code: some code: some code: some code                                                " + glb_new_line_symbol)
        file_handler.write("some code: 'some code: some code: some code                                               " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [0])
        self.assertEqual({}, a_dictionary["declares"])

    def test_scenario_2(self):
        # DECLARE count on the line is larger than 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write("'DECLARE x():                                                                             " + glb_new_line_symbol)
        file_handler.write("'DECLARE y(): DECLARE y():  DECLARE y():                                                  " + glb_new_line_symbol)
        file_handler.write("DECLARE z(a): DECLARE z(b):                                                               " + glb_new_line_symbol)
        file_handler.write("DECLARE w(a): 'DECLARE w():                                                               " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [1])
        self.assertEqual({'w': {'line': 6, 'parameters': ['a']}}, a_dictionary["declares"])

    def test_scenario_3(self):
        # Syntax errors
        file_handler = open(glb_input_filename, "w")
        file_handler.write("      DECLARE x():                                                                        " + glb_new_line_symbol)
        file_handler.write("    DECLARE     x    (    )    :                                                          " + glb_new_line_symbol)
        file_handler.write("some code: DECLARE z(x) ' DECLARE z ( x )                                                 " + glb_new_line_symbol)
        file_handler.write("some code: DECLARE z(x): ' DECLARE z ( x )                                                " + glb_new_line_symbol)
        file_handler.write("DECLARE                                                                                   " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name                                                                            " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name(                                                                           " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name (                                                                          " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name)                                                                           " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name )                                                                          " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_1(x)                                                                       " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_1b )x(                                                                     " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_2 (x)                                                                      " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_3 ( x )                                                                    " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name 4(a)                                                                       " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name 5 (a)                                                                      " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name6(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)                                  " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name7(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)                             " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name7               4 (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)            " + glb_new_line_symbol)
        file_handler.write("    DECLARE    a_name8      (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,                     " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8])
        self.assertEqual({}, a_dictionary["declares"])

    def test_scenario_4(self):
        # duplicated procedure declaration - uniqueness
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE z(a):                                                                              " + glb_new_line_symbol)
        file_handler.write("DECLARE z():                                                                              " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [6])
        self.assertEqual({'z': {'line': 3, 'parameters': ['a']}}, a_dictionary["declares"])

    def test_scenario_5(self):
        # maximum number of parameters exceeded
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11):                                 " + glb_new_line_symbol)
        file_handler.write("DECLARE y (v1, v2, v3, v4, v5, v6$, v7, v8, v9, v10):                                     " + glb_new_line_symbol)
        file_handler.write("DECLARE z (v1):                                                                           " + glb_new_line_symbol)
        file_handler.write("DECLARE w ():                                                                             " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [5])
        self.assertEqual({'y': {'line': 4, 'parameters': ['v1', 'v2', 'v3', 'v4', 'v5', 'v6$', 'v7', 'v8', 'v9', 'v10']},
                          'z': {'line': 7, 'parameters': ['v1']},
                          'w': {'line': 9, 'parameters': []}},
                         a_dictionary["declares"])

    def test_scenario_6(self):
        # missing parameters
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x (v1, v2, , v4):                                                                 " + glb_new_line_symbol)
        file_handler.write("DECLARE y (, , , ):                                                                       " + glb_new_line_symbol)
        file_handler.write("DECLARE z (v1,):                                                                           " + glb_new_line_symbol)
        file_handler.write("DECLARE w (,):                                                                             " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [3, 3, 3, 3, 3, 3, 3, 3])
        self.assertEqual({'x': {'line': 3, 'parameters': ['v1', 'v2', 'v4']},
                          'y': {'line': 5, 'parameters': []},
                          'z': {'line': 8, 'parameters': ['v1']},
                          'w': {'line': 10, 'parameters': []}},
                         a_dictionary["declares"])

    def test_scenario_7(self):
        # missing parameters
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x (v1, v1):                                                                       " + glb_new_line_symbol)
        file_handler.write("DECLARE y (v2$, v2$):                                                                     " + glb_new_line_symbol)
        file_handler.write("DECLARE z (v1, v2$):                                                                      " + glb_new_line_symbol)
        file_handler.write("DECLARE w ():                                                                             " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_output_filename, a_dictionary)
        self.assertEqual(an_error_list, [4, 4])
        self.assertEqual({'x': {'line': 3, 'parameters': ['v1']},
                          'y': {'line': 6, 'parameters': ['v2$']},
                          'z': {'line': 9, 'parameters': ['v1', 'v2$']},
                          'w': {'line': 11, 'parameters': []}},
                         a_dictionary["declares"])


if __name__ == '__main__':
    unittest.main()
