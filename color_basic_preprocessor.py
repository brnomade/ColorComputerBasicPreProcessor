import argparse
import configparser
import logging
import os
import subprocess
import string
import itertools
import re
from collections import deque


# configuration file handling
glb_folder_root = os.getcwd()
glb_script_configuration_filename = os.path.join(glb_folder_root, os.path.basename(__file__).split(".")[0] + ".ini")
# log file handling
glb_msg_prefix_try = "Trying to"
glb_msg_prefix_fail = "Failed to"
glb_msg_prefix_ok = "Succeeded to"
glb_script_log_filename = os.path.join(glb_folder_root, os.path.basename(__file__).split(".")[0] + ".log")
logging.basicConfig(filename=glb_script_log_filename, level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(process)d | %(thread)d | %(module)s | %(lineno)d |"
                           " %(funcName)s | %(message)s",
                    datefmt='%m/%d/%Y %I:%M:%S %p')
#
glb_available_numeric_references = deque([])
for item in itertools.product(string.ascii_uppercase + string.digits, repeat=2):
    if not item[0].isdigit():
        glb_available_numeric_references.append(item[0] + item[1])
#
glb_available_string_references = deque([])
for item in itertools.product(string.ascii_uppercase + string.digits, repeat=2):
    if not item[0].isdigit():
        glb_available_string_references.append(item[0] + item[1] + "$")
#
glb_max_available_parameters_for_procedures = 10
#
glb_available_procedure_numeric_parameters = list()
glb_available_procedure_string_parameters = list()
for counter in range(1, glb_max_available_parameters_for_procedures):
    glb_available_procedure_numeric_parameters.append(glb_available_numeric_references.pop())
    glb_available_procedure_string_parameters.append(glb_available_string_references.pop())
#
glb_empty_symbol = ""
glb_comment_symbol = "'"
glb_open_parenthesis_symbol = "("
glb_close_parenthesis_symbol = ")"
glb_dollar_symbol = "$"
glb_underscore_symbol = "_"
glb_colon_symbol = ":"
glb_equal_symbol = "="
glb_comma_symbol = ","
glb_new_line_symbol = "\n"
#
glb_no_error_code = 0
#
glb_error_messages = ["no errors found",
                      "multiple DECLARE keywords used on same line.",
                      "missing procedure definition after DECLARE keyword.",
                      "missing opening parentheses in procedure definition.",
                      "missing closing parentheses in procedure definition.",
                      "number of parameters in procedure exceeds " + str(glb_max_available_parameters_for_procedures) + ".",
                      ""]
# DECLARE related error codes
glb_error_declare_multiple = 1
glb_error_declare_missing_definition = 2
glb_error_declare_missing_opening_parenthesis = 3
glb_error_declare_missing_closing_parenthesis = 4
glb_error_declare_parameters_exceeded = 5



def present_script_section(a_section_name: str):
    print("")
    print("------------------------")
    print(a_section_name.upper())
    print("------------------------")


def present_script_title():
    print("")
    print("")
    print("CBPP - Color Basic Pre-Processor VERSION 0.1")
    print("Copyright(C) 2019 by Andre Ballista - www.oddpathsconsulting.co.uk")


def present_script_settings(a_configuration, the_arguments):
    # present the settings
    present_script_section("SETTINGS")
    print("input file:", the_arguments.input_file)
    print("output file:", the_arguments.output_file)
    print("bpp_phase:", the_arguments.bpp_phase)
    print("------------------------")
    print("")


def initialise_script_arguments_parser():
    parser = argparse.ArgumentParser(description="Analyse and process an input file coded in ColorBasic and output a new version of the file with the pre-processing requirements resolved.")
    parser.add_argument("input_file", help="file name of the input file. file extension expected. a full file path can be provided with the file name")
    parser.add_argument("output_file", help="file name of the output file. file extension expected. a full file path can be provided with the file name")
    parser.add_argument("-bpp_phase", choices=['NO', 'YES'], default='YES', help="Executes BPP as step 0 to resolve includes and pragmas. Default value is YES.")
    return parser


def initialise_script_configuration_parser():
    # Initialise the configuration parser
    config = configparser.ConfigParser()
    config.read(glb_script_configuration_filename)
    return config


def remove_empty_lines(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if a_line.strip() != "":
                output_file_handler.write(a_line)
    output_file_handler.close()


def execute_bpp(an_input_file_name, an_output_file_name):
    # execute bpp
    os_command = "bpp.exe" + " " + an_input_file_name
    os_command = os_command + " " + an_output_file_name
    try:
        subprocess.run(os_command, shell=True)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)


def present_error_message(a_line, a_line_number, an_error_code):
    # TODO potential parameters:
    # TODO - showing the original line
    # TODO - showing only the error code but not the error message
    # TODO - not showing any error message on screen
    print("syntax error", an_error_code, "line", a_line_number, glb_error_messages[an_error_code], a_line)


def process_procedure_declaration(an_input_file_name, an_output_file_name):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            declare_count = a_line.count("DECLARE")
            if declare_count == 0:
                output_file_handler.write(a_line)
            elif declare_count > 1:
                error_list.append(glb_error_declare_multiple)
                output_file_handler.write(a_line)
                present_error_message(a_line, line_number, glb_error_declare_multiple)
            else:
                a_line_splitted = a_line.rpartition("DECLARE")
                if glb_comment_symbol in a_line_splitted[0]:
                    # TODO - potential parameter - remove commented line from output
                    output_file_handler.write(a_line)
                elif a_line_splitted[2].strip() == glb_empty_symbol:
                    error_list.append(glb_error_declare_missing_definition)
                    output_file_handler.write(a_line)
                    present_error_message(a_line, line_number, glb_error_declare_missing_definition)
                elif glb_open_parenthesis_symbol not in a_line_splitted[2]:
                    error_list.append(glb_error_declare_missing_opening_parenthesis)
                    output_file_handler.write(a_line)
                    present_error_message(a_line, line_number, glb_error_declare_missing_opening_parenthesis)
                elif glb_close_parenthesis_symbol not in a_line_splitted[2]:
                    error_list.append(glb_error_declare_missing_closing_parenthesis)
                    output_file_handler.write(a_line)
                    present_error_message(a_line, line_number, glb_error_declare_missing_closing_parenthesis)
                else:
                    a_procedure_declaration = a_line_splitted[2].strip()
                    a_procedure_name = a_procedure_declaration.split(glb_open_parenthesis_symbol)[0].strip()
                    # TODO - potential paramter - add original line as a comment
                    output_file_handler.write(glb_comment_symbol + a_line)
                    output_file_handler.write(glb_underscore_symbol + a_procedure_name + glb_colon_symbol + glb_new_line_symbol)
                    a_parameter_list_declaration = a_procedure_declaration.split(glb_open_parenthesis_symbol)[1].strip().strip(glb_close_parenthesis_symbol).strip()
                    if len(a_parameter_list_declaration) > 0:
                        a_list_of_parameters = a_parameter_list_declaration.split(glb_comma_symbol)
                        if len(a_list_of_parameters) > glb_max_available_parameters_for_procedures:
                            error_list.append(glb_error_declare_parameters_exceeded)
                            output_file_handler.write(a_line)
                            present_error_message(a_line, line_number, glb_error_declare_parameters_exceeded)
                        else:
                            output_file_handler.write("LET ")
                            numeric_parameter_counter = 0
                            string_parameter_counter = 0
                            a_new_line = glb_empty_symbol
                            for a_parameter in a_list_of_parameters:
                                if a_parameter.strip()[-1] == glb_dollar_symbol:
                                    a_new_line = a_new_line + a_parameter.strip() + glb_equal_symbol + glb_available_procedure_string_parameters[string_parameter_counter] + glb_colon_symbol
                                    string_parameter_counter = string_parameter_counter + 1
                                else:
                                    a_new_line = a_new_line + a_parameter.strip() + glb_equal_symbol + glb_available_procedure_numeric_parameters[numeric_parameter_counter] + glb_colon_symbol
                                    numeric_parameter_counter = numeric_parameter_counter + 1
                            a_new_line = a_new_line.rstrip(glb_colon_symbol)
                            output_file_handler.write(a_new_line)
                            output_file_handler.write(glb_new_line_symbol)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def add_line_numbers_to_output_file(an_input_file_name, an_output_file_name):
    line_number = 10
    line_increment = 5
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            output_file_handler.write(str(line_number) + " " + a_line)
            line_number = line_number + line_increment
    output_file_handler.close()


def prepare_goto_and_gosub_references(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    reference_dictionary = dict()
    line_number = 1
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            a_line_splitted = a_line.rstrip().split(" ")
            # print(a_line_splitted)
            a_line_number = a_line_splitted[0]
            a_reference_name = a_line_splitted[1][0:-1]
            a_prefix = a_line_splitted[1][0]
            a_terminator = a_line_splitted[1][-1]
            if a_prefix == "_":
                if a_terminator == ":":
                    if a_reference_name in reference_dictionary.keys():
                        print("syntax error - line", line_number, "Duplicated GOTO/GOSUB reference name found.", a_line)
                    reference_dictionary[a_reference_name] = a_line_number
                    output_file_handler.write(a_line_number + " " + "'" + a_reference_name + "\n")
                else:
                    print("syntax error - line", line_number, "missing terminator after destination reference name", a_line)
            else:
                output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()
    # print(reference_dictionary)
    return reference_dictionary


def resolve_goto_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # Scenarios:
    # scenario 01 -> VALID -> 10 SOME CODE:GOTO somewhere
    # scenario 02 -> VALID -> 10 SOME CODE: GOTO somewhere
    # scenario 03 -> VALID -> 10 GOTO somewhere
    # scenario 04 -> VALID -> 10 SOME CODE: GOTO_somewhere
    # scenario 05 -> VALID -> 10 SOME CODE:GOTO_somewhere
    # scenario 06 -> ERROR -> 10 GOTO [blank] missing the target
    # scenario 07 -> ERROR -> 10 GOTO undefined_somewhere
    # scenario 08 -> NO ACTION -> 10 ' whatever GOTO whatever
    # scenario 09 -> VALID -> 10 SOME CODE: GOTO _somewhere 'A COMMENT
    # scenario 10 -> INVALID -> 10 SOME CODE: GOTO somewhere: GOTO somewhere else
    output_file_handler = open(an_output_file_name, "w")
    line_number = 1
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if "GOTO" in a_line:
                a_line_splitted = a_line.rpartition("GOTO")
                if "'" in a_line_splitted[0]:
                    # scenario 8
                    print("line", line_number, "- commented line - skipping.")
                elif a_line.count("GOTO") > 1:
                    # scenario 10
                    print("syntax error - line", line_number, "Multiple GOTO statements in a single line found.", a_line)
                elif a_line_splitted[2].strip() == "":
                    # scenario 6
                    print("syntax error - line", line_number, "GOTO reference missing.", a_line)
                else:
                    a_reference_name = a_line_splitted[2].strip().split(" ")[0]
                    if a_reference_name in a_reference_dictionary:
                        # scenarios 1, 2, 3, 4, 5 and 9.
                        a_line = a_line.replace(a_reference_name, str(a_reference_dictionary[a_reference_name]))
                    else:
                        # scenario 7
                        print("syntax error - line", line_number, "GOTO reference undefined.", a_line)
            output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()


def resolve_gosub_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # Scenarios:
    # scenario 01 -> VALID -> 10 SOME CODE:GOSUB somewhere
    # scenario 02 -> VALID -> 10 SOME CODE: GOSUB somewhere
    # scenario 03 -> VALID -> 10 GOSUB somewhere
    # scenario 04 -> VALID -> 10 SOME CODE: GOSUB_somewhere
    # scenario 05 -> VALID -> 10 SOME CODE:GOSUB_somewhere
    # scenario 06 -> ERROR -> 10 GOSUB [blank] missing the target
    # scenario 07 -> ERROR -> 10 GOSUB undefined_somewhere
    # scenario 08 -> NO ACTION -> 10 ' whatever GOSUB whatever
    # scenario 09 -> VALID -> 10 SOME CODE: GOSUB _somewhere 'A COMMENT
    # scenario 10 -> VALID -> 10 GOSUB here: GOSUB there: GOSUB futher:
    # scenario 11 -> VALID -> 10 GOSUB _somewhere:GOSUB_somewhere:GOSUB_somewhere"
    # scenario 12 -> VALID ->10 GOSUB _somewhere 'GOSUB _somewhere: GOSUB _somewhere"
    output_file_handler = open(an_output_file_name, "w")
    line_number = 1
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if "GOSUB" in a_line:
                a_line_splitted = a_line.rpartition("GOSUB")
                if "'" in a_line_splitted[0]:
                    # scenario 8
                    print("line", line_number, "- commented line - skipping.")
                elif a_line.count("GOSUB") > 1:
                    # scenario 10, 11 and 12
                    for a_slice_of_line in a_line.split(":"):
                        a_split = a_slice_of_line.rpartition("GOSUB")
                        if a_split[1].strip() == "GOSUB":
                            a_reference_name = a_split[2].strip()
                            if a_reference_name == "":
                                # scenario 6
                                print("syntax error - line", line_number, "GOSUB reference missing.", a_line, "column", a_slice_of_line)
                            elif a_reference_name in a_reference_dictionary:
                                a_line = a_line.replace(a_reference_name, str(a_reference_dictionary[a_reference_name]))
                            else:
                                # scenario 7
                                print("syntax error - line", line_number, "GOSUB reference undefined.", a_line, "column", a_slice_of_line)
                elif a_line_splitted[2].strip() == "":
                    # scenario 6
                    print("syntax error - line", line_number, "GOSUB reference missing.", a_line)
                else:
                    a_reference_name = a_line_splitted[2].strip().split(" ")[0]
                    if a_reference_name in a_reference_dictionary:
                        # scenarios 1, 2, 3, 4, 5 and 9.
                        a_line = a_line.replace(a_reference_name, str(a_reference_dictionary[a_reference_name]))
                    else:
                        # scenario 7
                        print("syntax error - line", line_number, "GOSUB reference undefined.", a_line)
            output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()


def prepare_variables_references(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    reference_dictionary = dict()
    line_number = 1
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if a_line.count("LET") > 1:
                print("syntax error - line", line_number, "multiple LET keywords used on same line.", a_line)
            elif a_line.count("LET") == 1:
                    for a_variable_definition in a_line.rpartition("LET")[2].split(":"):
                        if "=" not in a_variable_definition:
                            print("syntax error - line", line_number, "missing = symbol in variable definition", a_line)
                        else:
                            a_variable_name = a_variable_definition.split("=")[0].strip()
                            if a_variable_name[-1] == "$":
                                if len(glb_available_string_references) == 0:
                                    print("syntax error - line", line_number, "maximum number of string variables exceeded.", a_line)
                                else:
                                    reference_dictionary[a_variable_name] = glb_available_string_references.popleft()
                            else:
                                if len(glb_available_numeric_references) == 0:
                                    print("syntax error - line", line_number, "maximum number of numeric variables exceeded.", a_line)
                                else:
                                    reference_dictionary[a_variable_name] = glb_available_numeric_references.popleft()
            output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()
    # print(reference_dictionary)
    return reference_dictionary


def multi_word_replace(an_input_text, an_input_dictionary):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    taken from https://www.daniweb.com/programming/software-development/code/216636/multiple-word-replace-in-text-python
    """
    rc = re.compile('|'.join(map(re.escape, an_input_dictionary)))

    def translate(match):
        return an_input_dictionary[match.group(0)]
    #
    return rc.sub(translate, an_input_text)


def resolve_variables_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        all_input_file_lines = input_file_handler.read()
    #
    output_temp = multi_word_replace(all_input_file_lines, a_reference_dictionary)
    #
    output_file_handler.write(output_temp)
    output_file_handler.close()


def final_pass(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            output_file_handler.write(a_line)
    output_file_handler.close()


if __name__ == "__main__":
    # execute only if run as a script

    # Script starts
    input_arguments = initialise_script_arguments_parser().parse_args()
    configuration = initialise_script_configuration_parser()
    logging.info("**** Color Basic Preprocessor started ")
    #
    my_status = [glb_no_error_code]
    #
    source_filename_without_extension = input_arguments.input_file.split(".")[0]

    # run the BPP preprocessor
    input_filename = input_arguments.input_file
    output_filename = source_filename_without_extension + ".st1"
    execute_bpp(input_filename, output_filename)

    present_script_title()
    present_script_settings(configuration, input_arguments)

    # Process procedure declarations
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st2"
        my_status = process_procedure_declaration(input_filename, output_filename)

    # Remove empty lines from the source file
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st3"
        remove_empty_lines(input_filename, output_filename)

    # add line numbers to file
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st4"
        add_line_numbers_to_output_file(input_filename, output_filename)

    # prepare goto and gosub references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st5"
        a_dictionary = prepare_goto_and_gosub_references(input_filename, output_filename)

    # resolve goto references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st6"
        resolve_goto_references(input_filename, output_filename, a_dictionary)

    # resolve gosub references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st7"
        resolve_gosub_references(input_filename, output_filename, a_dictionary)

    # prepare variables references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st8"
        a_dictionary = prepare_variables_references(input_filename, output_filename)

    # prepare variables references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st9"
        resolve_variables_references(input_filename, output_filename, a_dictionary)

    # final pass
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = input_arguments.output_file
        final_pass(input_filename, output_filename)
