import unittest
from color_basic_preprocessor import prepare_variables_references, resolve_variables_references, initialise_a_reference_dictionary, initialise_available_numeric_references_list, initialise_available_string_references_list
from color_basic_preprocessor import glb_new_line_symbol, glb_no_error_code
import os

glb_input_filename = "in_resolve_variables_references.txt"
glb_intermediate_filename = "mid_resolve_variables_references.txt"
glb_output_filename = "out_resolve_variables_references.txt"
param_remove_file_after_test = False


class TestResolveVariablesReferences(unittest.TestCase):

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
        # file is empty, file has empty lines, file has lines with only spaces, file has no variables being used
        file_handler = open(glb_input_filename, "w")
        file_handler.write("")
        file_handler.write(glb_new_line_symbol)
        file_handler.write("                                                                                          " + glb_new_line_symbol)
        file_handler.write("some code: some code: some code: some code                                                " + glb_new_line_symbol)
        file_handler.write("some code: 'some code: some code: some code                                               " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references = initialise_available_numeric_references_list()
        an_available_string_references = initialise_available_string_references_list()
        an_error_list = prepare_variables_references(glb_input_filename, glb_intermediate_filename, a_dictionary, an_available_numeric_references, an_available_string_references)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = resolve_variables_references(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list[0], glb_no_error_code)
            self.assertEqual(an_error_list[1], 0)
            self.assertEqual({}, a_dictionary["variables"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_2(self):
        # lines include comments and empty lines
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET x:                                                                                    " + glb_new_line_symbol)
        file_handler.write(" LET y: LET z: ' LET w :                                                                  " + glb_new_line_symbol)
        file_handler.write("' LET x: LET y: LET z: LET w :                                                            " + glb_new_line_symbol)
        file_handler.write("                                                                                          " + glb_new_line_symbol)
        file_handler.write("  LET x$ : LET y$: LET z$ : LET w$:                                                       " + glb_new_line_symbol)
        file_handler.write(" ' LET a_very_long_name_with_0123 : LET a_very_long_name_with_0123$:                      " + glb_new_line_symbol)
        file_handler.write(" ' some code : some code : some code : LET abc :                                          " + glb_new_line_symbol)
        file_handler.write("   LET p: LET p$                                                                          " + glb_new_line_symbol)
        file_handler.write("LET t : LET t$:                                                                             " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references = initialise_available_numeric_references_list()
        an_available_string_references = initialise_available_string_references_list()
        an_error_list = prepare_variables_references(glb_input_filename, glb_intermediate_filename, a_dictionary, an_available_numeric_references, an_available_string_references)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = resolve_variables_references(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list[0], glb_no_error_code)
            self.assertEqual(an_error_list[1], 10)
            self.assertEqual({'x': 'AA',
                              'y': 'AB', 'z': 'AC',
                              'x$': 'AA$', 'y$': 'AB$', 'z$': 'AC$', 'w$': 'AD$',
                              'p': 'AD',
                              't': 'AE',
                              't$': 'AE$'},
                             a_dictionary["variables"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_3(self):
        # easy examples
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET x:                                                                                    " + glb_new_line_symbol)
        file_handler.write("x = x + x - x * x / x + (x - x)                                                           " + glb_new_line_symbol)
        file_handler.write("x = 1 + x                                                                                 " + glb_new_line_symbol)
        file_handler.write("x=1+x                                                                                     " + glb_new_line_symbol)
        file_handler.write("PRINT x                                                                                   " + glb_new_line_symbol)
        file_handler.write("GOSUB x                                                                                   " + glb_new_line_symbol)
        file_handler.write("GOTO x + 1 : GOSUB 1 + x: GOSUB x                                                         " + glb_new_line_symbol)
        file_handler.write("GOTO 1 + x                                                                                " + glb_new_line_symbol)
        file_handler.write("DRAW(x, x, x, x)                                                                          " + glb_new_line_symbol)
        file_handler.write("PAINT(x, x, x, x, x, x, x, x, x, x, x, x, x, x, x,xy,yx,yxz,xyz,yzx,                      " + glb_new_line_symbol)
        file_handler.write("ON     x     GOTO     x                                                                   " + glb_new_line_symbol)

        file_handler.write("DRAW(x + x, x, xy, x, x, x, x, x,x,x  x , x, x, x,xy,yx,yxz,xyz,yzx,xx,xxx,xxxx,x):x      " + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references = initialise_available_numeric_references_list()
        an_available_string_references = initialise_available_string_references_list()
        an_error_list = prepare_variables_references(glb_input_filename, glb_intermediate_filename, a_dictionary, an_available_numeric_references, an_available_string_references)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = resolve_variables_references(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list[0], glb_no_error_code)
            self.assertEqual(an_error_list[1], 56)
            self.assertEqual({'x': 'AA'}, a_dictionary["variables"])
        else:
            self.fail("error on pre-condition method.")

    def test_scenario_4(self):
        # know errors in the code
        file_handler = open(glb_input_filename, "w")
        file_handler.write("LET x:                                                                                    " + glb_new_line_symbol)
        file_handler.write('PRINT "x"                                                                                 ' + glb_new_line_symbol)
        file_handler.write('PRINT "maximiliam     had     an  x-man in his  x-pocket full of x rays"                  ' + glb_new_line_symbol)
        file_handler.close()
        a_dictionary = initialise_a_reference_dictionary()
        an_available_numeric_references = initialise_available_numeric_references_list()
        an_available_string_references = initialise_available_string_references_list()
        an_error_list = prepare_variables_references(glb_input_filename, glb_intermediate_filename, a_dictionary, an_available_numeric_references, an_available_string_references)
        if an_error_list[0] == glb_no_error_code:
            an_error_list = resolve_variables_references(glb_intermediate_filename, glb_output_filename, a_dictionary)
            self.assertEqual(an_error_list[0], glb_no_error_code)
            self.assertEqual(an_error_list[1], 5)
            self.assertEqual({'x': 'AA'}, a_dictionary["variables"])
        else:
            self.fail("error on pre-condition method.")

    def xtest_scenario_3(self):
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

    def xtest_scenario_4(self):
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

    def xtest_scenario_5(self):
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

    def xtest_scenario_6(self):
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

    def xtest_scenario_7(self):
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

    def xtest_scenario_8(self):
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

    def xtest_scenario_9(self):
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

    def xtest_scenario_10(self):
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
