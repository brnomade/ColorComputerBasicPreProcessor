from unittest import TestCase
from color_basic_preprocessor import process_procedure_declaration

glb_new_line_symbol = "\n"
glb_input_filename = "declare_unit_test_input.txt"
glb_output_filename = "declare_unit_test_output.txt"

class TestProcessProcedureDeclaration(TestCase):
    """" Tests for procedure declaration """


    def setUp( self ):
        output_file_handler = open(glb_input_filename, "w")
        output_file_handler.write("'DECLARE" + glb_new_line_symbol)
        output_file_handler.write("DECLARE" + glb_new_line_symbol)
        output_file_handler.write("DECLARE x(): DECLARE y()" + glb_new_line_symbol)
        output_file_handler.write("DECLARE x() ': DECLARE y()" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name(" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name (" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name)" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name )" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name(x)" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name (x)" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name()" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name ()" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)" + glb_new_line_symbol)
        output_file_handler.write("DECLARE a_name (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)" + glb_new_line_symbol)
        output_file_handler.write(
            "DECLARE a_procedure_with_a_very_very_very_very_very_long_name(my_param_1, my_param_2, my_param_3, a_very_long_param, my_param_1$)" + glb_new_line_symbol)
        output_file_handler.write(
            "DECLARE a_procedure_with_a_very_very_very_very_very_long_name (my_param_1, my_param_2, my_param_3, a_very_long_param, my_param_1$)" + glb_new_line_symbol)
        output_file_handler.close()


    def tearDown( self ):
        # not sure what needs to be done
        print("should delete the test file")


    def test_process_procedure_declaration( self ):
        error_codes_list = process_procedure_declaration(glb_input_filename, glb_output_filename)
        self.assertTrue(error_codes_list == [2, 1, 1, 3, 4, 4, 3, 3, 5, 5])


if __name__ == '__main__':
    unittest.main()
