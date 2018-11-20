from sys import *
from copy import deepcopy

import yaml

from .inputtype import InputType
from .test import Test
from mph.program import Program

from fuzzbang.alphanumericfuzzer import AlphaNumericFuzzer

def yaml2data(yaml_data):
    data = {}
    fields = yaml_data.keys()

    if "target_arguments" in fields:
        data[InputType.ARGV] = deepcopy(yaml_data["target_arguments"])

    if "target_stdin_type" in fields:
        if yaml_data["target_stdin_type"] == "literal":
            if "target_stdin" in fields:
                data[InputType.STDIN] = yaml_data["target_stdin"]
        else:
            custom_fuzzer_name = yaml_data["target_stdin_type"]
            custom_fuzzer_params = tuple(yaml_data["target_stdin"])

            eval_string = custom_fuzzer_name + str(custom_fuzzer_params) + ".generate()"
            print(eval_string) # DEBUG
            data[InputType.STDIN] = eval(eval_string)

    return data

def main():
    if len(argv) != 2: # usage
        print("usage: lm5 config_file")
        exit(-1)

    config_file_path = argv[1]
   
    # read config file
    with open(config_file_path, "r") as f:
        config_file_contents = f.read()
    
    # parse configuration file contents as YAML
    yaml_data = yaml.load(config_file_contents)
    config_data = yaml2data(yaml_data)
    test_types = list(config_data.keys())

    # initialise test
    target_path = yaml_data["target_path"]
    target = Program(target_path, [])
    test = Test(target, test_types)
    test.from_config(config_data)

    # run test
    print("Running test \"{0}\"...".format(test.name))
    target_retval, target_stdout, target_stderr = test.run()
    print(target_retval, target_stdout, target_stderr) # DEBUG
    print("Test \"{0}\" ran successfully.".format(test.name))

    # display test results
    print("Target at {0} exited with status {1}".format(target_path,
        target_retval))
    print("Target said this on STDOUT:")
    print(" "*8 + target_stdout.decode("utf-8"))
    
    print("Target said this on STDERR:")
    print(" "*8 + target_stderr.decode("utf-8"))

if __name__ == "__main__":
    main()

