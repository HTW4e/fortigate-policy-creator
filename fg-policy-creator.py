#!/usr/bin/env python3
'''
Copyright (C) 2019  HTW4e <htw4e@htw4e.li>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# import global mondule
import os
import csv
import configparser

# global variables
filename = "fg-ruleset.txt"
total_rows = 0

# function to create blank ruleset file
def create_ruleset_file():
    # import modules for this function
    import datetime

    # define some variables as global
    global filename

    now = datetime.datetime.now()
    time_now = now.strftime("%Y%m%d-%H%M")
    filename = "fg-ruleset_" + time_now + ".txt"

    # create file only if not exist
    if not os.path.isfile(filename):
        os.mknod(filename)

# function to count rows in csv file
def count_rows_in_csv(config):

    csv_rule_file = config.get('Policy', 'rules-file')

    # define some variables as global
    global total_rows

    total_rows = 0
    with open(csv_rule_file, 'r') as f:
        for line in f:
            total_rows += 1

    # remove header row
    total_rows -= 1

# function to create rule from jinja2 template
def create_fg_policyrules(config, POLICY_NUMBER, POLICY_NAME, SRC_INTERFACE, DST_INTERFACE, SRC_ADDRESS, DST_ADDRESS, SERVICE_NAME, NEXT_ACTION):
    # import modules for this function
    from jinja2 import Environment, FileSystemLoader

    policy_template_file = config.get('Policy', 'policy-template')

    this_dir = os.path.dirname(os.path.abspath(__file__))

    j2_env = Environment(loader=FileSystemLoader(this_dir), trim_blocks=True)
    rule = j2_env.get_template(policy_template_file).render(
        POLICY_NUMBER = POLICY_NUMBER,
        POLICY_NAME = POLICY_NAME,
        SRC_INTERFACE = SRC_INTERFACE,
        DST_INTERFACE = DST_INTERFACE,
        SRC_ADDRESS = SRC_ADDRESS,
        DST_ADDRESS = DST_ADDRESS,
        SERVICE_NAME = SERVICE_NAME,
        NEXT_ACTION = NEXT_ACTION
    )

    # write rule to file
    f = open(filename, 'a')
    f.write(rule + '\n')
    f.close()

# function to create rules from csv file
def create_rules(config):
    # variables
    count = 1
    csv_rule_file = config.get('Policy', 'rules-file')
    FIRST_POLICY_NUMBER = config.get('Policy', 'first_policy_number')

    with open(csv_rule_file) as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        for row in reader:
            values = dict(zip(header,row))

            POLICY_NUMBER = FIRST_POLICY_NUMBER
            POLICY_NAME = values.get('POLICY_NAME')
            SRC_INTERFACE = values.get('SRC_INTERFACE')
            DST_INTERFACE = values.get('DST_INTERFACE')
            SRC_ADDRESS = values.get('SRC_ADDRESS')
            DST_ADDRESS = values.get('DST_ADDRESS')
            SERVICE_NAME = values.get('SERVICE_NAME')
            if total_rows > count:
                NEXT_ACTION = 'next'
            else:
                NEXT_ACTION = 'end'

            create_fg_policyrules(config, POLICY_NUMBER, POLICY_NAME, SRC_INTERFACE, DST_INTERFACE, SRC_ADDRESS, DST_ADDRESS, SERVICE_NAME, NEXT_ACTION)

            FIRST_POLICY_NUMBER = int(FIRST_POLICY_NUMBER) + 1
            count += 1

# main function
def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    count_rows_in_csv(config)
    create_ruleset_file()
    create_rules(config)

# main program
if __name__ == '__main__':
    main()
