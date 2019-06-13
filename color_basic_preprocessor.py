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
# glb_script_log_filename = os.path.join(glb_folder_root, os.path.basename(__file__).split(".")[0] + ".log")
# logging.basicConfig(filename=glb_script_log_filename, level=logging.DEBUG,
#                    format="%(asctime)s %(levelname)s: %(process)d | %(thread)d | %(module)s | %(lineno)d |"
#                           " %(funcName)s | %(message)s",
#                    datefmt='%m/%d/%Y %I:%M:%S %p')
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
glb_line_number_start = 10
glb_line_number_increment = 5
#
glb_available_procedure_numeric_parameters = list()
glb_available_procedure_string_parameters = list()
for counter in range(0, glb_max_available_parameters_for_procedures):
    glb_available_procedure_numeric_parameters.append(glb_available_numeric_references.pop())
    glb_available_procedure_string_parameters.append(glb_available_string_references.pop())
#
glb_keyword_goto = "GOTO"
glb_keyword_gosub = "GOSUB"
glb_keyword_declare = "DECLARE"
#
glb_empty_symbol = ""
glb_comment_symbol = "'"
glb_space_symbol = " "
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
                      "duplicate procedure name found.",
                      "procedure name contains invalid character.",
                      "",
                      "",
                      "duplicate GOTO/GOSUB reference name found.",
                      "missing terminator for GOTO/GOSUB reference name.",
                      "missing line number before GOTO/GOSUB reference.",
                      "GOTO/GOSUB reference name contains invalid character.",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "Multiple GOTO statements in a single line found.",
                      "GOTO reference missing or incorrectly defined.",
                      "GOTO reference unknown.",
                      "missing prefix on GOTO reference name.",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "GOSUB reference missing or incorrectly defined.",
                      "GOSUB reference unknown.",
                      "missing prefix on GOSUB reference name."]

# DECLARE related error codes
glb_error_declare_multiple = 1
glb_error_declare_missing_definition = 2
glb_error_declare_missing_opening_parenthesis = 3
glb_error_declare_missing_closing_parenthesis = 4
glb_error_declare_parameters_exceeded = 5
glb_error_declare_duplicate_definition = 6
glb_error_declare_contains_invalid_character = 7

# GOTO / GOSUB definition related error codes
glb_error_gotogosub_duplicate_reference = 10
glb_error_gotogosub_missing_terminator = 11
glb_error_gotogosub_missing_line_number = 12
glb_error_gotogosub_contains_invalid_character = 13

# GOTO resolution related error codes
glb_error_goto_multiple_found = 20
glb_error_goto_undefined_reference = 21
glb_error_goto_unknown_reference = 22
glb_error_goto_malformed_reference_name = 23

# GOSUB resolution related error codes
glb_error_gosub_undefined_reference = 30
glb_error_gosub_unknown_reference = 31
glb_error_gosub_malformed_reference_name = 32

#
glb_reference_dictionary = dict()
glb_reference_dictionary["declares"] = dict()
glb_reference_dictionary["gotogosub"] = dict()
#


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
    a_basic_line_number = a_line.split(glb_space_symbol)[0].strip()
    if a_basic_line_number.isnumeric():
        a_line_number = a_basic_line_number
    print(a_line, "^---", "syntax error #" + str(an_error_code), "on line", a_line_number, ": " + glb_error_messages[an_error_code])
    print()


def handle_syntax_error(an_error_code, a_line_number, a_line, an_error_list, a_file_handler):
    # TODO - potential option to keep the reference as comment and used it as a target or remove the line and use as target the next line
    param_write_error_line_into_output_file = True
    an_error_list.append(an_error_code)
    if param_write_error_line_into_output_file:
        a_file_handler.write(a_line)
    present_error_message(a_line, a_line_number, an_error_code)
    return an_error_list


def remove_empty_lines(an_input_file_name, an_output_file_name):
    error_list = list()
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if not a_line.strip() == glb_empty_symbol:
                output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def process_procedure_declaration(an_input_file_name, an_output_file_name, a_reference_dictionary):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            declare_count = a_line.count(glb_keyword_declare)
            if declare_count == 0:
                output_file_handler.write(a_line)
            elif declare_count > 1:
                error_list = handle_syntax_error(glb_error_declare_multiple, line_number, a_line, error_list, output_file_handler)
                # error_list.append(glb_error_declare_multiple)
                # output_file_handler.write(a_line)
                # present_error_message(a_line, line_number, glb_error_declare_multiple)
            else:
                a_line_split = a_line.rpartition(glb_keyword_declare)
                if glb_comment_symbol in a_line_split[0]:
                    # TODO - potential parameter - remove commented line from output
                    output_file_handler.write(a_line)
                elif a_line_split[2].strip() == glb_empty_symbol:
                    error_list = handle_syntax_error(glb_error_declare_missing_definition, line_number, a_line, error_list, output_file_handler)
                    # error_list.append(glb_error_declare_missing_definition)
                    # output_file_handler.write(a_line)
                    # present_error_message(a_line, line_number, glb_error_declare_missing_definition)
                elif glb_open_parenthesis_symbol not in a_line_split[2]:
                    error_list = handle_syntax_error(glb_error_declare_missing_opening_parenthesis, line_number, a_line, error_list, output_file_handler)
                    # error_list.append(glb_error_declare_missing_opening_parenthesis)
                    # output_file_handler.write(a_line)
                    # present_error_message(a_line, line_number, glb_error_declare_missing_opening_parenthesis)
                elif glb_close_parenthesis_symbol not in a_line_split[2]:
                    error_list = handle_syntax_error(glb_error_declare_missing_closing_parenthesis, line_number, a_line, error_list, output_file_handler)
                    # error_list.append(glb_error_declare_missing_closing_parenthesis)
                    # output_file_handler.write(a_line)
                    # present_error_message(a_line, line_number, glb_error_declare_missing_closing_parenthesis)
                else:
                    a_procedure_declaration = a_line_split[2].strip()
                    a_procedure_name = a_procedure_declaration.split(glb_open_parenthesis_symbol)[0].strip()
                    if glb_space_symbol in a_procedure_name:
                        error_list = handle_syntax_error(glb_error_declare_contains_invalid_character, line_number, a_line, error_list, output_file_handler)
                        # error_list.append(glb_error_declare_contains_invalid_character)
                        # output_file_handler.write(a_line)
                        # present_error_message(a_line, line_number, glb_error_declare_contains_invalid_character)
                    elif a_procedure_name in a_reference_dictionary["declares"].keys():
                        error_list = handle_syntax_error(glb_error_declare_duplicate_definition, line_number, a_line, error_list, output_file_handler)
                        # error_list.append(glb_error_declare_duplicate_definition)
                        # output_file_handler.write(a_line)
                        # present_error_message(a_line, line_number, glb_error_declare_duplicate_definition)
                    else:
                        a_reference_dictionary["declares"][a_procedure_name] = line_number
                        # TODO - potential parameter - add original line as a comment
                        output_file_handler.write(glb_comment_symbol + a_line)
                        output_file_handler.write(glb_underscore_symbol + a_procedure_name + glb_colon_symbol + glb_new_line_symbol)
                        a_parameter_list_declaration = a_procedure_declaration.split(glb_open_parenthesis_symbol)[1].strip().strip(glb_close_parenthesis_symbol).strip()
                        if len(a_parameter_list_declaration) > 0:
                            a_list_of_parameters = a_parameter_list_declaration.split(glb_comma_symbol)
                            if len(a_list_of_parameters) > glb_max_available_parameters_for_procedures:
                                error_list = handle_syntax_error(glb_error_declare_parameters_exceeded, line_number, a_line, error_list, output_file_handler)
                                # error_list.append(glb_error_declare_parameters_exceeded)
                                # output_file_handler.write(a_line)
                                # present_error_message(a_line, line_number, glb_error_declare_parameters_exceeded)
                            else:
                                output_file_handler.write("LET ")
                                numeric_parameter_counter = 0
                                string_parameter_counter = 0
                                a_new_line = glb_empty_symbol
                                # print(a_list_of_parameters)
                                for a_parameter in a_list_of_parameters:
                                    if a_parameter.strip()[-1] == glb_dollar_symbol:
                                        # print(a_parameter, numeric_parameter_counter, string_parameter_counter)
                                        a_new_line = a_new_line + a_parameter.strip() + glb_equal_symbol + glb_available_procedure_string_parameters[string_parameter_counter] + glb_colon_symbol
                                        string_parameter_counter = string_parameter_counter + 1
                                    else:
                                        # print(a_parameter, numeric_parameter_counter, numeric_parameter_counter)
                                        # print(glb_available_procedure_numeric_parameters)
                                        a_new_line = a_new_line + a_parameter.strip() + glb_equal_symbol + glb_available_procedure_numeric_parameters[numeric_parameter_counter] + glb_colon_symbol
                                        numeric_parameter_counter = numeric_parameter_counter + 1
                                a_new_line = a_new_line.rstrip(glb_colon_symbol)
                                output_file_handler.write(a_new_line)
                                output_file_handler.write(glb_new_line_symbol)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def add_line_numbers(an_input_file_name, an_output_file_name):
    error_list = list()
    line_number = glb_line_number_start
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            output_file_handler.write(str(line_number) + glb_space_symbol + a_line)
            line_number = line_number + glb_line_number_increment
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def prepare_goto_and_gosub_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # goto and gosub references are represented as _<a label>:
    # the reference is expected to be at the start of a line
    # reference names cannot contain spaces
    # line numbers are expected to exist on the line
    # references are expected to be alone on the line. no further code is expected to exist on the same line.
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            if len(a_line.strip()) > 0:
                a_line_number = a_line.split(glb_space_symbol)[0].strip()
                if a_line_number.isnumeric():
                    a_reference_name = a_line.rpartition(a_line_number)[2].strip()
                    if a_reference_name == glb_empty_symbol:
                        # scenario - the line has nothing after the line number
                        output_file_handler.write(a_line)
                    elif a_reference_name[0] == glb_underscore_symbol:
                        if glb_space_symbol in a_reference_name:
                            # scenario - the potential reference is incorrectly named or more code is on the same line
                            error_list = handle_syntax_error(glb_error_gotogosub_contains_invalid_character, line_number, a_line, error_list, output_file_handler)
                        elif a_reference_name[-1] == glb_colon_symbol:
                            if a_reference_name in a_reference_dictionary["gotogosub"].keys():
                                # scenario - the potential reference has been previously used
                                error_list = handle_syntax_error(glb_error_gotogosub_duplicate_reference, line_number, a_line, error_list, output_file_handler)
                            else:
                                a_reference_dictionary["gotogosub"][a_reference_name] = a_line_number
                                output_file_handler.write(a_line_number + glb_space_symbol + glb_comment_symbol + a_reference_name + glb_new_line_symbol)
                        else:
                            # scenario - the potential reference ends with something different than colon :
                            error_list = handle_syntax_error(glb_error_gotogosub_missing_terminator, line_number, a_line, error_list, output_file_handler)
                    else:
                        # scenario - the potential reference starts with something different than underscore _
                        output_file_handler.write(a_line)
                else:
                    # scenario - the line does not start with a line number
                    error_list = handle_syntax_error(glb_error_gotogosub_missing_line_number, line_number, a_line, error_list, output_file_handler)
            else:
                # scenario - the line is completely empty
                output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def resolve_goto_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # Scenarios:
    # scenario 01  -> 10 GOTO somewhere
    # scenario 02  -> 10 SOME CODE: GOTO somewhere
    # scenario 03  -> 10 SOME CODE:  GOTO somewhere: SOME MORE CODE HERE
    # scenario 06  -> 10 GOTO [blank] - target is empty
    # scenario 07  -> 10 GOTO [undefined_somewhere] - target is not empty but has not been declared previously
    # scenario 08a -> 10 ' whatever GOTO whatever
    # scenario 08b -> 10 SOME CODE: GOTO _somewhere 'A COMMENT
    # scenario 08c -> 10 GOTO _somewhere ' GOTO somewhere GOTO somewhere
    # scenario 10a -> 10 SOME CODE: GOTO somewhere: GOTO somewhere else
    # scenario 10b -> 10 GOTO somewhere: GOTO somewhere else : SOME CODE
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            if glb_keyword_goto in a_line:
                if glb_comment_symbol in a_line:
                    # scenario 8
                    # identify if the GOTO keyword is located to the left of the comment symbol. i.e.: 10 GOTO 20 '
                    position_of_comment_symbol = a_line.find(glb_comment_symbol)
                    a_line_split = a_line[0: position_of_comment_symbol]
                    # print("comment found",position_of_comment_symbol,a_line_split)
                else:
                    a_line_split = a_line
                if a_line_split.count(glb_keyword_goto) > 1:
                    # scenario 10
                    error_list = handle_syntax_error(glb_error_goto_multiple_found, line_number, a_line, error_list, output_file_handler)
                    # error_list.append(glb_error_goto_multiple_found)
                    # output_file_handler.write(a_line)
                    # present_error_message(a_line, line_number, glb_error_goto_multiple_found)
                elif a_line_split.count(glb_keyword_goto) == 1:
                    result = re.search("GOTO(.+?:)?", a_line_split).group(1)
                    # if result is None:
                    #     print("regex returns: None")
                    # else:
                    #     print("regex returns:", result)
                    if result is None:
                        # scenario 6
                        error_list = handle_syntax_error(glb_error_goto_undefined_reference, line_number, a_line, error_list, output_file_handler)
                        # error_list.append(glb_error_goto_undefined_reference)
                        # output_file_handler.write(a_line)
                        # present_error_message(a_line, line_number, glb_error_goto_undefined_reference)
                    else:
                        a_reference_name = result.strip()
                        if not (a_reference_name[0] == glb_underscore_symbol) or not (a_reference_name[-1] == glb_colon_symbol):
                            # print("found: [" + a_reference_name + "]")
                            error_list = handle_syntax_error(glb_error_goto_malformed_reference_name, line_number, a_line, error_list, output_file_handler)
                            # error_list.append(glb_error_goto_malformed_reference_name)
                            # output_file_handler.write(a_line)
                            # present_error_message(a_line, line_number, glb_error_goto_malformed_reference_name)
                        else:
                            if a_reference_name in a_reference_dictionary["gotogosub"].keys():
                                # scenarios 1,2,3.
                                a_line = a_line.replace(a_reference_name, a_reference_dictionary["gotogosub"][a_reference_name], 1)
                            else:
                                # scenario 7
                                # print("found: [" + a_reference_name + "]")
                                error_list = handle_syntax_error(glb_error_goto_unknown_reference, line_number, a_line, error_list, output_file_handler)
                                # error_list.append(glb_error_goto_unknown_reference)
                                # output_file_handler.write(a_line)
                                # present_error_message(a_line, line_number, glb_error_goto_unknown_reference)
            output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def resolve_gosub_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # Scenarios:
    # scenario 01  -> 10 GOSUB somewhere
    # scenario 02  -> 10 SOME CODE: GOSUB somewhere
    # scenario 03  -> 10 SOME CODE:  GOSUB somewhere: SOME MORE CODE HERE
    # scenario 06  -> 10 GOSUB [blank] - target is empty
    # scenario 07  -> 10 GOSUB [undefined_somewhere] - target is not empty but has not been declared previously
    # scenario 08a -> 10 ' whatever GOSUB whatever
    # scenario 08b -> 10 SOME CODE: GOSUB _somewhere 'A COMMENT
    # scenario 08c -> 10 GOSUB _somewhere ' GOSUB somewhere GOSUB somewhere
    # scenario 10a -> 10 SOME CODE: GOSUB somewhere: GOSUB somewhere else
    # scenario 10b -> 10 GOSUB somewhere: GOSUB somewhere else : SOME CODE
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            if glb_comment_symbol in a_line:
                # scenario 8
                # identify if the GOSUB keyword is located to the left of the comment symbol. i.e.: 10 GOSUB 20 '
                position_of_comment_symbol = a_line.find(glb_comment_symbol)
                a_line_split = a_line[0: position_of_comment_symbol]
                # print("comment found",position_of_comment_symbol,a_line_split)
            else:
                a_line_split = a_line
            if glb_keyword_gosub in a_line_split:
                result = re.findall("GOSUB(.+?:)?", a_line_split)
                # if not result:
                #     print("regex returns: None")
                # else:
                #     print("regex returns:", result)
                for a_reference_name in result:
                    a_strip_reference_name = a_reference_name.strip()
                    if a_strip_reference_name == glb_empty_symbol:
                        # scenario 6
                        error_list = handle_syntax_error(glb_error_gosub_undefined_reference, line_number, a_line,error_list, output_file_handler)
                        # error_list.append(glb_error_gosub_undefined_reference)
                        # output_file_handler.write(a_line)
                        # present_error_message(a_line, line_number, glb_error_gosub_undefined_reference)
                    elif not (a_strip_reference_name[0] == glb_underscore_symbol) or not (a_strip_reference_name[-1] == glb_colon_symbol):
                        error_list = handle_syntax_error(glb_error_gosub_malformed_reference_name, line_number, a_line,error_list, output_file_handler)
                        # error_list.append(glb_error_gosub_malformed_reference_name)
                        # output_file_handler.write(a_line)
                        # present_error_message(a_line, line_number, glb_error_gosub_malformed_reference_name)
                    elif a_strip_reference_name in a_reference_dictionary["gotogosub"].keys():
                        # scenarios 1,2,3.
                        a_line = a_line.replace(a_strip_reference_name, a_reference_dictionary["gotogosub"][a_strip_reference_name], 1)
                    else:
                        # scenario 7
                        # print("found: [" + a_reference_name + "]")
                        error_list = handle_syntax_error(glb_error_gosub_unknown_reference, line_number, a_line,error_list, output_file_handler)
                        # error_list.append(glb_error_gosub_unknown_reference)
                        # output_file_handler.write(a_line)
                        # present_error_message(a_line, line_number, glb_error_gosub_unknown_reference)
            output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


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


def main():
    # Script starts
    input_arguments = initialise_script_arguments_parser().parse_args()
    configuration = initialise_script_configuration_parser()
    # logging.info("**** Color Basic Preprocessor started ")
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

    # Remove empty lines from the source file
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st2"
        my_status = remove_empty_lines(input_filename, output_filename)

    # Process procedure declarations
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st3"
        my_status = process_procedure_declaration(input_filename, output_filename, glb_reference_dictionary)

    # add line numbers to file
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st4"
        my_status = add_line_numbers(input_filename, output_filename)

    # prepare goto and gosub references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st5"
        my_status = prepare_goto_and_gosub_references(input_filename, output_filename, glb_reference_dictionary)

    print(glb_reference_dictionary)
    exit()


    # resolve goto references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st6"
        my_status = resolve_goto_references(input_filename, output_filename, glb_reference_dictionary)

    # resolve gosub references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st7"
        resolve_gosub_references(input_filename, output_filename, glb_reference_dictionary)

    print(glb_reference_dictionary)
    exit()

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


if __name__ == "__main__":
    # execute only if run as a script
    main()

# TODO - how to handle On BRK GOTO a line number
# TODO - how to handle ON ERR GOTO line number
# TODO - how to handle ON variable GOSUB line1, line2, line3
# TODO - how to handle ON variable GOTO line1, line2, line3
