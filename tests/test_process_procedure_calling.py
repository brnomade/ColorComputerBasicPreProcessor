import unittest
from color_basic_preprocessor import process_procedure_declaration, process_procedure_calling, initialise_a_reference_dictionary
from color_basic_preprocessor import glb_new_line_symbol, glb_no_error_code
import os

glb_input_filename = "in_process_procedure_calling.txt"
glb_intermediate_filename = "mid_process_procedure_calling.txt"
glb_output_filename = "out_process_procedure_calling.txt"
param_remove_file_after_test = True

class TestProcessProcedureCalling(unittest.TestCase):

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
        if os.path.exists(glb_intermediate_filename):
            if param_remove_file_after_test:
                os.remove(glb_intermediate_filename)
        else:
            print("can't find file", glb_intermediate_filename, ". will not delete it.")
        if os.path.exists(glb_output_filename):
            if param_remove_file_after_test:
                os.remove(glb_output_filename)
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")

    def test_scenario_1(self):
        # file is empty, file has empty lines, file has lines with only spaces, file has no procedures being called
        file_handler = open(glb_input_filename, "w")
        file_handler.write("")
        file_handler.write(glb_new_line_symbol)
        file_handler.write("                                                                                          " + glb_new_line_symbol)
        file_handler.write("some code: some code: some code: some code                                                " + glb_new_line_symbol)
        file_handler.write("some code: 'some code: some code: some code                                               " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [0])
            self.assertEqual({}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_2(self):
        # CALL count on the line is larger than 1
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE z(a):                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL z(a): 'CALL z(a):  CALL z(a):                                                        " + glb_new_line_symbol)
        file_handler.write("CALL z(a): CALL z(b):                                                                     " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [50])
            self.assertEqual({'z': {'line': 3, 'parameters': ['a']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_3(self):
        # Syntax errors
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x(a,b):                                                                           " + glb_new_line_symbol)
        file_handler.write("      CALL x(1,2                                                                          " + glb_new_line_symbol)
        file_handler.write("    CALL x 1,2)                                                                           " + glb_new_line_symbol)
        file_handler.write("    CALL (x 1,2)                                                                          " + glb_new_line_symbol)
        file_handler.write("some code: CALL x(x, ' CALL z ( x )                                                       " + glb_new_line_symbol)
        file_handler.write("some code: CALL x x,y): ' CALL z ( x )                                                    " + glb_new_line_symbol)
        file_handler.write("CALL                                                                                      " + glb_new_line_symbol)
        file_handler.write("CALL x                                                                                    " + glb_new_line_symbol)
        file_handler.write("CALL x(                                                                                   " + glb_new_line_symbol)
        file_handler.write("CALL x)                                                                                   " + glb_new_line_symbol)
        file_handler.write("CALL x )                                                                                  " + glb_new_line_symbol)
        file_handler.write("CALL x (                                                                                  " + glb_new_line_symbol)
        file_handler.write("CALL x )x(                                                                                " + glb_new_line_symbol)
        file_handler.write("CALL x(10, 'A', t, my variable_1):                                                        " + glb_new_line_symbol)
        file_handler.write("CALL x y z (10, 'A', t, my_variable_1):                                                   " + glb_new_line_symbol)
        file_handler.write("CALL x.y.z (10, 'A', t, my_variable_1):                                                   " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55])
            self.assertEqual({'x': {'line': 3, 'parameters': ['a', 'b']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_4(self):
        # call to unknown procedure
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x(a,b):                                                                           " + glb_new_line_symbol)
        file_handler.write("CALL y(1,2)                                                                               " + glb_new_line_symbol)
        file_handler.write("CALL y (1,2)                                                                              " + glb_new_line_symbol)
        file_handler.write("CALL y (1,)                                                                               " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [51, 51, 51])
            self.assertEqual({'x': {'line': 3, 'parameters': ['a', 'b']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_5(self):
        # maximum number of parameters exceeded
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x(a,b):                                                                           " + glb_new_line_symbol)
        file_handler.write("CALL x(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)                                      " + glb_new_line_symbol)
        file_handler.write("CALL x (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)                                     " + glb_new_line_symbol)
        file_handler.write("CALL x (v1, , v3, v4, v5, v6, v7, v8, v9, v10, v11)                                       " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [52, 52, 52])
            self.assertEqual({'x': {'line': 3, 'parameters': ['a', 'b']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_6(self):
        # parameter numbers mismatch
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x(a,b):                                                                           " + glb_new_line_symbol)
        file_handler.write("CALL x(v1, v2, v3)                                                                        " + glb_new_line_symbol)
        file_handler.write("CALL x (v1, , v3)                                                                         " + glb_new_line_symbol)
        file_handler.write("CALL x (v1)                                                                               " + glb_new_line_symbol)
        file_handler.write("CALL x ()                                                                                 " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [53, 53, 53, 53])
            self.assertEqual({'x': {'line': 3, 'parameters': ['a', 'b']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_7(self):
        # parameters missing
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x(a,b):                                                                           " + glb_new_line_symbol)
        file_handler.write("CALL x (v1, )                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL x (,v2)                                                                              " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [57, 57])
            self.assertEqual({'x': {'line': 3, 'parameters': ['a', 'b']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_8(self):
        # expected string but parameter is numeric
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x ( b$ ):                                                                         " + glb_new_line_symbol)
        file_handler.write("CALL x (\"A\")                                                                            " + glb_new_line_symbol)
        file_handler.write("CALL x ( a$ )                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL x ( 123 )                                                                            " + glb_new_line_symbol)
        file_handler.write("CALL x ( a )                                                                              " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [54, 54])
            self.assertEqual({'x': {'line': 3, 'parameters': ['b$']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_9(self):
        # expected numeric but parameter is string
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x ( b ):                                                                           " + glb_new_line_symbol)
        file_handler.write("CALL x (\"A\")                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL x ( a$ )                                                                              " + glb_new_line_symbol)
        file_handler.write("CALL x ( 123 )                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL x ( a )                                                                               " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [56, 56])
            self.assertEqual({'x': {'line': 3, 'parameters': ['b']}}, a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_10(self):
        # valid calls
        file_handler = open(glb_input_filename, "w")
        file_handler.write("DECLARE x ( b ):                                                                           " + glb_new_line_symbol)
        file_handler.write("DECLARE y ( b$ ):                                                                          " + glb_new_line_symbol)
        file_handler.write("DECLARE z (p1, p2$, p3):                                                                   " + glb_new_line_symbol)
        file_handler.write("CALL x ( 123 )                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL x ( a )                                                                               " + glb_new_line_symbol)
        file_handler.write("CALL y (\"A\")                                                                             " + glb_new_line_symbol)
        file_handler.write("CALL y ( a$ )                                                                              " + glb_new_line_symbol)
        file_handler.write("CALL z ( a, b$, c )                                                                        " + glb_new_line_symbol)
        file_handler.write("CALL z ( 123, \"HELLO\", 456 )                                                             " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_error_list = process_procedure_declaration(glb_input_filename, glb_intermediate_filename, a_dictionary)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = process_procedure_calling(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list, [0])
            self.assertEqual({'x': {'line': 3, 'parameters': ['b']},
                              'y': {'line': 6, 'parameters': ['b$']},
                             'z': {'line': 9, 'parameters': ['p1', 'p2$', 'p3']}},
                             a_dictionary["declares"])
        else:
            self.fail("error on pre-condition method.")


if __name__ == '__main__':
    unittest.main()
