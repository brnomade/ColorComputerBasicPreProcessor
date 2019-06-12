import unittest
from color_basic_preprocessor import process_procedure_declaration, glb_new_line_symbol, glb_reference_dictionary
import os

glb_input_filename = "unit_test_input.txt"
glb_output_filename = "unit_test_output.txt"


class TestProcessProcedureDeclaration(unittest.TestCase):

    def setUp(self):
        file_handler = open(glb_input_filename, "w")
        file_handler.write("'DECLARE" + glb_new_line_symbol)
        file_handler.write("DECLARE" + glb_new_line_symbol)
        file_handler.write("DECLARE x(): DECLARE y()" + glb_new_line_symbol)
        file_handler.write("DECLARE x() ': DECLARE y()" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name(" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name (" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name)" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name )" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_1(x)" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_2 (x)" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name_3 ( x ) " + glb_new_line_symbol)
        file_handler.write("DECLARE a_name 4()" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name 5 ()" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name6(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name7(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)" + glb_new_line_symbol)
        file_handler.write("DECLARE a_name7               4 (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)" + glb_new_line_symbol)
        file_handler.write("              DECLARE              a_name8               (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)" + glb_new_line_symbol)
        file_handler.write("              DECLARE              a_name8               (         v1, v2, v3, v4,          v5, v6, v7, v8, v9,          v10      )" + glb_new_line_symbol)
        file_handler.write("DECLARE a_procedure_with_a_very_very_very_very_very_long_name(my_param_1, my_param_2, my_param_3, a_very_long_param, my_param_1$)" + glb_new_line_symbol)
        file_handler.write("DECLARE a_procedure_with_a_very_very_very_very_very_long_name something wrong     (my_param_1, my_param_2, my_param_3, a_very_long_param, my_param_1$)" + glb_new_line_symbol)
        file_handler.write("DECLARE y                     (my_param_1, my_param_2, my_param_3, a_very_long_param, my_param_1$)" + glb_new_line_symbol)
        file_handler.write("                  DECLARE      y                     (my_param_1, my_param_2, my_param_3, a_very_long_param, my_param_1$)" + glb_new_line_symbol)
        file_handler.close()

    def tearDown(self):
        if os.path.exists(glb_input_filename):
            os.remove(glb_input_filename)
        else:
            print("can't find file", glb_input_filename, ". will not delete it.")
        if os.path.exists(glb_output_filename):
            os.remove(glb_output_filename)
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")


    def test_process_procedure_declaration(self):
        error_codes_list = process_procedure_declaration(glb_input_filename, glb_output_filename, glb_reference_dictionary)
        self.assertTrue(error_codes_list == [2, 1, 1, 3, 4, 4, 3, 3, 7, 7, 5, 7, 5, 6, 7, 6])


if __name__ == '__main__':
    unittest.main()
