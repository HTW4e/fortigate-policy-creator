#!/usr/bin/env python3
# import global modules
import os

# variables
this_dir = os.path.dirname(os.path.abspath(__file__))

# function to read csv file
def read_csv_file():
    # import function
    import csv

    # variables
    csv_rule_file = 'rules.csv'

    with open(csv_rule_file) as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        for row in reader:
            print(dict(zip(header,row)))

# function to create rule from jinja2 template
def create_fg_policyrules():
    # import modules for this function
    from jinja2 import Environment, FileSystemLoader

    # variables
    policy_template_file = 'policy-template.jinja2'

    j2_env = Environment(loader=FileSystemLoader(this_dir), trim_blocks=True)
    rule = j2_env.get_template(policy_template_file).render(
        POLICY_NUMBER = '100',
        POLICY_NAME = 'Test Policy',
        SRC_INTERFACE = 'LAN',
        DST_INTERFACE = 'WAN',
        SRC_ADDRESS = '10.10.10.10',
        DST_ADDRESS = '8.8.8.8',
        SERVICE_NAME = 'HTTP'
    )

    print(rule)

# main function
def main():
    read_csv_file()
    #create_fg_policyrules()

# main program
if __name__ == '__main__':
    main()
