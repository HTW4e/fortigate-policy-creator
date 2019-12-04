#!/usr/bin/env python3
# Copyright (C) 2019  HTW4e <htw4e@htw4e.li>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# import global modules
import os

# function to create rule from jinja2 template
def create_fg_policyrules(POLICY_NAME, SRC_INTERFACE, DST_INTERFACE, SRC_ADDRESS, DST_ADDRESS, SERVICE_NAME):
    # import modules for this function
    from jinja2 import Environment, FileSystemLoader

    # variables
    policy_template_file = 'policy-template.jinja2'

    this_dir = os.path.dirname(os.path.abspath(__file__))

    j2_env = Environment(loader=FileSystemLoader(this_dir), trim_blocks=True)
    rule = j2_env.get_template(policy_template_file).render(
        POLICY_NUMBER = '100',
        POLICY_NAME = POLICY_NAME,
        SRC_INTERFACE = SRC_INTERFACE,
        DST_INTERFACE = DST_INTERFACE,
        SRC_ADDRESS = SRC_ADDRESS,
        DST_ADDRESS = DST_ADDRESS,
        SERVICE_NAME = SERVICE_NAME
    )

    print(rule)

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
            values = dict(zip(header,row))

            POLICY_NAME = values.get('POLICY_NAME')
            SRC_INTERFACE = values.get('SRC_INTERFACE')
            DST_INTERFACE = values.get('DST_INTERFACE')
            SRC_ADDRESS = values.get('SRC_ADDRESS')
            DST_ADDRESS = values.get('DST_ADDRESS')
            SERVICE_NAME = values.get('SERVICE_NAME')

            create_fg_policyrules(POLICY_NAME, SRC_INTERFACE, DST_INTERFACE, SRC_ADDRESS, DST_ADDRESS, SERVICE_NAME)

# main function
def main():
    read_csv_file()

# main program
if __name__ == '__main__':
    main()
