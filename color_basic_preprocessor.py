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
glb_max_available_parameters_for_procedures = 10
glb_line_number_start = 10
glb_line_number_increment = 5
#
# glb_available_numeric_references = deque([])
# for item in itertools.product(string.ascii_uppercase + string.digits, repeat=2):
#     if not item[0].isdigit():
#         glb_available_numeric_references.append(item[0] + item[1])
#
# glb_available_string_references = deque([])
# for item in itertools.product(string.ascii_uppercase + string.digits, repeat=2):
#     if not item[0].isdigit():
#         glb_available_string_references.append(item[0] + item[1] + "$")
#
# glb_available_procedure_numeric_parameters = list()
# glb_available_procedure_string_parameters = list()
# for counter in range(0, glb_max_available_parameters_for_procedures):
#     glb_available_procedure_numeric_parameters.append(glb_available_numeric_references.pop())
#     glb_available_procedure_string_parameters.append(glb_available_string_references.pop())
#

glb_keyword_goto = "GOTO"
glb_keyword_gosub = "GOSUB"
glb_keyword_declare = "DECLARE"
glb_keyword_call = "CALL"
glb_keyword_end = "END"
glb_keyword_let = "LET"
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
glb_double_quote_symbol = '"'
glb_number_0_symbol = "0"
#
glb_no_error_code = 0
#
glb_error_messages = ["no errors found",
                      "multiple DECLARE keywords used on same line.",
                      "missing procedure definition after DECLARE keyword.",
                      "missing parameter in procedure definition.",
                      "parameter is already used in procedure declaration.",
                      "number of parameters in procedure exceeds " + str(glb_max_available_parameters_for_procedures) + ".",
                      "duplicate procedure name found.",
                      "procedure name contains invalid character.",
                      "syntax error on procedure declaration",
                      "",
                      "duplicate GOTO/GOSUB reference name found.",
                      "",
                      "",
                      "",
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
                      "missing prefix on GOSUB reference name.",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "Variable undefined.",
                      "Variable unknown.",
                      "Syntax error on variable declaration.",
                      "maximum number of string variables exceeded",
                      "maximum number of numeric variables exceeded",
                      "duplicate variable name found.",
                      "incorrect variable name. variable name must be alpha numeric.",
                      "",
                      "",
                      "",
                      "multiple CALL keywords used on same line.",
                      "call to an undeclared procedure.",
                      "number of parameters exceeds " + str(glb_max_available_parameters_for_procedures) + ".",
                      "number of parameters mismatch procedure definition.",
                      "parameter type mismatch in procedure call, string expected.",
                      "syntax error on procedure call",
                      "parameter type mismatch in procedure call, numeric expected.",
                      ]

# DECLARE related error codes
glb_error_declare_multiple = 1
glb_error_declare_missing_definition = 2
glb_error_declare_missing_parameter = 3
glb_error_declare_parameter_already_used = 4
glb_error_declare_parameters_exceeded = 5
glb_error_declare_duplicate_definition = 6
glb_error_declare_contains_invalid_character = 7
glb_error_declare_invalid_syntax = 8

# GOTO / GOSUB definition related error codes
glb_error_gotogosub_duplicate_reference = 10

# GOTO resolution related error codes
glb_error_goto_multiple_found = 20
glb_error_goto_undefined_reference = 21
glb_error_goto_unknown_reference = 22
glb_error_goto_malformed_reference_name = 23

# GOSUB resolution related error codes
glb_error_gosub_undefined_reference = 30
glb_error_gosub_unknown_reference = 31
glb_error_gosub_malformed_reference_name = 32

# VARIABLES definition related error codes
glb_error_variable_undefined = 40
glb_error_variable_unknown = 41
glb_error_variable_malformed = 42
glb_error_variable_string_limit_reached = 43
glb_error_variable_numeric_limit_reached = 44
glb_error_variable_duplicate_reference = 45
glb_error_variable_numeric_named = 46

# CALL related error codes
glb_error_call_multiple = 50
glb_error_call_to_undeclared_procedure = 51
glb_error_call_parameters_exceeded = 52
glb_error_call_parameters_numbers_mismatch = 53
glb_error_call_parameters_type_error_string = 54
glb_error_call_invalid_syntax = 55
glb_error_call_parameters_type_error_numeric = 56


def initialise_a_reference_dictionary():
    a_reference_dictionary = dict()
    a_reference_dictionary["declares"] = dict()
    a_reference_dictionary["gotogosub"] = dict()
    a_reference_dictionary["variables"] = dict()
    return a_reference_dictionary


def initialise_available_numeric_references_list():
    a_collection = deque([])
    for item in itertools.product(string.ascii_uppercase + string.digits, repeat=2):
        if not item[0].isdigit():
            a_collection.append(item[0] + item[1])
    return a_collection


def initialise_available_string_references_list():
    a_collection = deque([])
    for item in itertools.product(string.ascii_uppercase + string.digits, repeat=2):
        if not item[0].isdigit():
            a_collection.append(item[0] + item[1] + "$")
    return a_collection


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
    param_write_error_line_into_output_file = False
    an_error_list.append(an_error_code)
    if param_write_error_line_into_output_file:
        a_file_handler.write(a_line)
    present_error_message(a_line, a_line_number, an_error_code)
    return an_error_list


def strip_comment_from_line(a_line):
    if glb_comment_symbol in a_line:
        # scenario - identify where the comment symbol is and return a line containing only the sequence before the symbol
        position_of_comment_symbol = a_line.find(glb_comment_symbol)
        a_line_split = a_line[0: position_of_comment_symbol]
    else:
        a_line_split = a_line
    return a_line_split


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


def line_number_from_file_line(a_file_line_number):
    a_file_line_number = int(a_file_line_number)
    return str(((a_file_line_number - 1) * glb_line_number_increment)  + glb_line_number_start)


def process_procedure_declaration(an_input_file_name, an_output_file_name, a_reference_dictionary):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            # scenario - identify if the keyword is located to the left of the comment symbol.
            a_line_strip = strip_comment_from_line(a_line)
            declare_count = a_line_strip.count(glb_keyword_declare)
            if declare_count == 0:
                output_file_handler.write(a_line)
            elif declare_count > 1:
                # scenario - only one DECLARE keyword per line is acceptable
                error_list = handle_syntax_error(glb_error_declare_multiple, line_number, a_line, error_list, output_file_handler)
            else:
                result = re.search("(^DECLARE)\s+([a-zA-Z_0-9]+)\s*(\()([a-zA-Z_0-9\,\s\$]*)(\)\s*:)", a_line_strip)
                if result is None:
                    error_list = handle_syntax_error(glb_error_declare_invalid_syntax, line_number, a_line, error_list, output_file_handler)
                else:
                    a_reserved_word = result.group(1)
                    a_procedure_name = result.group(2).strip()
                    a_prefix = result.group(3)
                    if result.group(4).strip() == glb_empty_symbol:
                        a_parameters_list = []
                    else:
                        a_parameters_list = result.group(4).strip().split(glb_comma_symbol)
                    a_sufix = result.group(5)
                    if a_procedure_name in a_reference_dictionary["declares"].keys():
                        error_list = handle_syntax_error(glb_error_declare_duplicate_definition, line_number, a_line, error_list, output_file_handler)
                    else:
                        if len(a_parameters_list) > glb_max_available_parameters_for_procedures:
                            error_list = handle_syntax_error(glb_error_declare_parameters_exceeded, line_number, a_line, error_list, output_file_handler)
                        else:
                            # comment the declaration line
                            output_file_handler.write(glb_keyword_end + glb_space_symbol + glb_comment_symbol + glb_space_symbol + a_line)
                            # include the declared procedure in the dictionary
                            a_reference_dictionary["declares"][a_procedure_name] = {"line": line_number, "parameters": []}
                            # process defined parameters
                            a_new_line = glb_empty_symbol
                            for a_parameter in a_parameters_list:
                                a_parameter = a_parameter.strip()
                                if not a_parameter.strip() == glb_empty_symbol:
                                    if a_parameter in a_reference_dictionary["declares"][a_procedure_name]["parameters"]:
                                        error_list = handle_syntax_error(glb_error_declare_parameter_already_used, line_number, a_line, error_list, output_file_handler)
                                    # elif a_parameter[-1] == glb_dollar_symbol:
                                    #    # a_new_line = a_new_line + glb_keyword_let + glb_space_symbol + a_parameter + glb_equal_symbol + glb_double_quote_symbol + glb_double_quote_symbol + glb_colon_symbol
                                    #    a_new_line = a_new_line + glb_keyword_let + glb_space_symbol + a_parameter + glb_colon_symbol
                                    #    a_reference_dictionary["declares"][a_procedure_name]["parameters"].append(a_parameter)
                                    else:
                                        # a_new_line = a_new_line + glb_keyword_let + glb_space_symbol + a_parameter + glb_equal_symbol + glb_number_0_symbol + glb_colon_symbol
                                        a_new_line = a_new_line + glb_keyword_let + glb_space_symbol + a_parameter + glb_colon_symbol
                                        a_reference_dictionary["declares"][a_procedure_name]["parameters"].append(a_parameter)
                                else:
                                    error_list = handle_syntax_error(glb_error_declare_missing_parameter, line_number, a_line, error_list, output_file_handler)
                            # output the list of parameters assignment
                            if not a_new_line.strip() == glb_empty_symbol:
                                output_file_handler.write(a_new_line + glb_new_line_symbol)
                                line_number = line_number + 1
                            # output the gosub reference
                            output_file_handler.write(glb_underscore_symbol + str(line_number) + glb_underscore_symbol + glb_keyword_declare + glb_underscore_symbol  + a_procedure_name + glb_colon_symbol + glb_new_line_symbol)
                            line_number = line_number + 1
                            a_reference_dictionary["declares"][a_procedure_name]["line"] = line_number
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def process_procedure_calling(an_input_file_name, an_output_file_name, a_reference_dictionary):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            # scenario - identify if the keyword is located to the left of the comment symbol.
            a_line_strip = strip_comment_from_line(a_line)
            keyword_count = a_line_strip.count(glb_keyword_call)
            # scenario - only one keyword per line is acceptable
            if keyword_count == 0:
                output_file_handler.write(a_line)
            elif keyword_count > 1:
                error_list = handle_syntax_error(glb_error_call_multiple, line_number, a_line, error_list, output_file_handler)
            else:
                result = re.search("(CALL)\s+([a-zA-Z_0-9]+)\s*(\()([a-zA-Z_0-9\$\"\,\s]*)(\)\s*)", a_line_strip)
                if result is None:
                    print(result)
                    error_list = handle_syntax_error(glb_error_call_invalid_syntax, line_number, a_line, error_list, output_file_handler)
                else:
                    a_reserved_word = result.group(1)
                    a_procedure_name = result.group(2).strip()
                    a_prefix = result.group(3)
                    a_parameters_list = result.group(4).split(glb_comma_symbol)
                    a_sufix = result.group(5)
                    if a_procedure_name not in a_reference_dictionary["declares"].keys():
                        error_list = handle_syntax_error(glb_error_call_to_undeclared_procedure, line_number, a_line, error_list, output_file_handler)
                    else:
                        if len(a_parameters_list) > glb_max_available_parameters_for_procedures:
                            error_list = handle_syntax_error(glb_error_call_parameters_exceeded, line_number, a_line, error_list, output_file_handler)
                        elif not len(a_parameters_list) == len(a_reference_dictionary["declares"][a_procedure_name]["parameters"]):
                            error_list = handle_syntax_error(glb_error_call_parameters_numbers_mismatch, line_number, a_line, error_list, output_file_handler)
                        else:
                            a_new_line = glb_empty_symbol
                            for parameter_index in range(0, len(a_parameters_list)):
                                a_parameter = a_reference_dictionary["declares"][a_procedure_name]["parameters"][parameter_index].strip()
                                a_value = a_parameters_list[parameter_index].strip()
                                if a_parameter[-1] == glb_dollar_symbol and (a_value.isnumeric() or a_value[-1] not in [glb_dollar_symbol, glb_double_quote_symbol]):
                                    error_list = handle_syntax_error(glb_error_call_parameters_type_error_string, line_number, a_line, error_list, output_file_handler)
                                elif (not a_parameter[-1] == glb_dollar_symbol) and (not a_value.isnumeric()) and (a_value[-1] in [glb_dollar_symbol, glb_double_quote_symbol]):
                                    error_list = handle_syntax_error(glb_error_call_parameters_type_error_numeric, line_number, a_line, error_list, output_file_handler)
                                else:
                                    a_new_line = a_new_line + a_parameter + glb_equal_symbol + a_value + glb_colon_symbol
                            output_file_handler.write(a_new_line + "GOSUB" + glb_space_symbol + glb_underscore_symbol + a_procedure_name + glb_colon_symbol + glb_space_symbol + glb_comment_symbol + a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def prepare_variables_references(an_input_file_name, an_output_file_name, a_reference_dictionary, a_numeric_variables_list, a_string_variables_list):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            a_line_strip = strip_comment_from_line(a_line)
            if "LET" in a_line_strip:
                result = re.finditer("(LET)\s+([a-zA-Z_0-9$]+)\s*(:)", a_line_strip)
                a_reference = None
                for a_reference in result:
                    a_reserved_word = a_reference.group(1).strip()
                    a_variable_name = a_reference.group(2).strip()
                    an_operator = a_reference.group(3).strip()
                    if a_variable_name == glb_empty_symbol:
                        # scenario - a variable name must not be empty
                        error_list = handle_syntax_error(glb_error_variable_malformed, line_number, a_line, error_list, output_file_handler)
                    elif a_variable_name.rstrip("$").isnumeric():
                        # scenario - a variable name must be alphanumeric
                        error_list = handle_syntax_error(glb_error_variable_numeric_named, line_number, a_line, error_list, output_file_handler)
                    elif a_variable_name in a_reference_dictionary["variables"].keys():
                        # scenario - a variable name must be unique
                        error_list = handle_syntax_error(glb_error_variable_duplicate_reference, line_number, a_line, error_list, output_file_handler)
                    elif a_variable_name[-1] == "$":
                        if not a_string_variables_list:
                            # scenario - number of variables declared exceeds the limit
                            error_list = handle_syntax_error(glb_error_variable_string_limit_reached, line_number, a_line, error_list, output_file_handler)
                        else:
                            a_reference_dictionary["variables"][a_variable_name] = a_string_variables_list.popleft()
                    else:
                        if not a_numeric_variables_list:
                            # scenario - number of variables declared exceeds the limit
                            error_list = handle_syntax_error(glb_error_variable_numeric_limit_reached, line_number, a_line, error_list, output_file_handler)
                        else:
                            a_reference_dictionary["variables"][a_variable_name] = a_numeric_variables_list.popleft()
                if a_reference is None:
                    # scenario - the line contains a LET statement but it does not follow a valid syntax
                    error_list = handle_syntax_error(glb_error_variable_malformed, line_number, a_line, error_list, output_file_handler)
            output_file_handler.write(a_line)
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
            a_line_strip = strip_comment_from_line(a_line)
            if not a_line_strip == glb_empty_symbol:
                # scenario - the line is not empty
                result = re.search("(^\s*)(_[a-zA-Z_0-9]+:)", a_line_strip)
                if result is not None:
                    a_reference_name = result.group(2).strip()
                    if a_reference_name in a_reference_dictionary["gotogosub"].keys():
                        # scenario - the potential reference has been previously used
                        error_list = handle_syntax_error(glb_error_gotogosub_duplicate_reference, line_number, a_line, error_list, output_file_handler)
                    else:
                        a_reference_dictionary["gotogosub"][a_reference_name] = {"file_line": str(line_number)}
                        a_line = glb_comment_symbol + a_line
            output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def resolve_variables_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    #
    joined_variables = '|'.join(map(re.escape, a_reference_dictionary["variables"]))
    rc = re.compile("(\s|=|:|\+|\*|\-|\/|\)|\(|^)(" + joined_variables + ")(\s|=|:|\+|\*|\-|\/|\)|\,|\n)")
    #
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            # scenario - identify if the keyword is located to the left of the comment symbol.
            position_of_comment_symbol = a_line.find(glb_comment_symbol)
            a_match = rc.search(a_line)
            while a_match is not None:
                if position_of_comment_symbol == -1 or (a_match.end(2) < position_of_comment_symbol):
                    a_line = "".join((a_line[:a_match.start(2)], a_reference_dictionary["variables"][a_match.group(2)], a_line[a_match.end(2):]))
                    a_match = rc.search(a_line)
                else:
                    a_match = None
            output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def resolve_goto_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            a_line_strip = strip_comment_from_line(a_line)
            if glb_keyword_goto in a_line_strip:
                if a_line_strip.count(glb_keyword_goto) > 1:
                    # scenario - multiple GOTOs on the same line
                    error_list = handle_syntax_error(glb_error_goto_multiple_found, line_number, a_line, error_list, output_file_handler)
                else:
                    result = re.search("(GOTO)\s+(\_)([a-zA-Z0-9_]+)(\:)", a_line_strip)
                    if result is not None:
                        a_reference_name = result.group(2).strip() + result.group(3).strip() + result.group(4).strip()
                        if a_reference_name in a_reference_dictionary["gotogosub"].keys():
                            a_line = a_line.replace(a_reference_name, line_number_from_file_line(a_reference_dictionary["gotogosub"][a_reference_name]["file_line"]), 1)
                        else:
                            # scenario - target is not empty but has not been declared previously
                            error_list = handle_syntax_error(glb_error_goto_unknown_reference, line_number, a_line, error_list, output_file_handler)
            output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


def resolve_gosub_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    line_number = 0
    error_list = list()
    #
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            line_number = line_number + 1
            a_line_strip = strip_comment_from_line(a_line)
            if glb_keyword_gosub in a_line_strip:
                result = re.finditer("(GOSUB)\s+(\_)([a-zA-Z0-9_]+)(\:)", a_line_strip)
                for a_reference in result:
                    a_reference_name = a_reference.group(2).strip() + a_reference.group(3).strip() + a_reference.group(4).strip()
                    if a_reference_name in a_reference_dictionary["gotogosub"].keys():
                        a_line = a_line.replace(a_reference_name, line_number_from_file_line(a_reference_dictionary["gotogosub"][a_reference_name]["file_line"]))
                    else:
                        # scenario - target is not empty but has not been declared previously
                        error_list = handle_syntax_error(glb_error_gosub_unknown_reference, line_number, a_line, error_list, output_file_handler)
            output_file_handler.write(a_line)
    output_file_handler.close()
    if len(error_list) == 0:
        error_list.append(glb_no_error_code)
    return error_list


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
    glb_reference_dictionary = initialise_a_reference_dictionary()
    glb_available_numeric_references = initialise_available_numeric_references_list()
    glb_available_string_references = initialise_available_string_references_list()
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
    source_filename_without_extension = input_arguments.input_file.split(".")[0]
    #
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
        my_status = process_procedure_declaration(input_filename, output_filename, glb_reference_dictionary)

    # Process procedure calling
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st3"
        my_status = process_procedure_calling(input_filename, output_filename, glb_reference_dictionary)

    # prepare variables references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st4"
        my_status = prepare_variables_references(input_filename, output_filename, glb_reference_dictionary, glb_available_numeric_references, glb_available_string_references)

    # prepare goto and gosub references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st5"
        my_status = prepare_goto_and_gosub_references(input_filename, output_filename, glb_reference_dictionary)

    # resolve variables references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st6"
        resolve_variables_references(input_filename, output_filename, glb_reference_dictionary)

    # add line numbers to file
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st7"
        my_status = add_line_numbers(input_filename, output_filename)

    # resolve goto references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st8"
        my_status = resolve_goto_references(input_filename, output_filename, glb_reference_dictionary)

    # resolve gosub references
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = source_filename_without_extension + ".st9"
        my_status = resolve_gosub_references(input_filename, output_filename, glb_reference_dictionary)

    # final pass
    if my_status[0] == glb_no_error_code:
        input_filename = output_filename
        output_filename = input_arguments.output_file
        final_pass(input_filename, output_filename)

    print(glb_reference_dictionary)

if __name__ == "__main__":
    # execute only if run as a script
    main()

# TODO - how to handle On BRK GOTO a line number
# TODO - how to handle ON ERR GOTO line number
# TODO - how to handle ON variable GOSUB line1, line2, line3
# TODO - how to handle ON variable GOTO line1, line2, line3
