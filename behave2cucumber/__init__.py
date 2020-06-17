'''
Copyright (c) 2016 Behalf Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


def convert(json_file, remove_background=False, duration_format=False, deduplicate=False, remove_empty=False):
    # json_nodes are the scopes available in behave/cucumber json: Feature -> elements(Scnerios) -> Steps
    json_nodes = ['feature', 'elements', 'steps']
    # These fields doesn't exist in cucumber report, there-fore when converting from behave, we need to delete these
    # fields.
    fields_not_exist_in_cucumber_json = ['status', 'step_type']

    def format_level(tree, index=0, id_counter=0):
        for item in tree:
            # Location in behave json translates to uri and line in cucumber json
            uri, line_number = item.pop("location").split(":")
            item["line"] = int(line_number)
            for field in fields_not_exist_in_cucumber_json:
                if field in item:
                    item.pop(field)
            if 'tags' in item:
                # Tags in behave are just a list of tag names, in cucumber every tag has a name and a line number.
                item['tags'] = [{"name": tag if tag.startswith('@') else '@' + tag, "line": item["line"] - 1} for tag in
                                item['tags']]
            if json_nodes[index] == 'steps':
                if 'result' in item:
                    # Because several problems with long error messages the message sub-stringed to maximum 2000 chars.
                    if 'error_message' in item["result"]:
                        error_msg = item["result"].pop('error_message')
                        item["result"]["error_message"] = str(
                            (str(error_msg).replace("\"", "").replace("\\'", ""))[:2000])
                    if 'duration' in item["result"] and duration_format:
                        item["result"]["duration"] = int(item["result"]["duration"] * 1000000000)
                else:
                    # In behave, skipped tests doesn't have result object in their json, there-fore when we generating
                    # Cucumber report for every skipped test we need to generated a new result with status skipped
                    item["result"] = {"status": "skipped", "duration": 0}
                if 'table' in item:
                    item['rows'] = []
                    t_line = 1
                    item['rows'].append({"cells": item['table']['headings'], "line": item["line"] + t_line})
                    for table_row in item['table']['rows']:
                        t_line += 1
                        item['rows'].append({"cells": table_row, "line": item["line"] + t_line})
            else:
                # uri is the name of the feature file the current item located
                item["uri"] = uri
                item["description"] = ""
                item["id"] = id_counter
                id_counter += 1
            # If the scope is not "steps" proceed with the recursion
            if index != 2 and json_nodes[index + 1] in item:
                item[json_nodes[index + 1]] = format_level(
                    item[json_nodes[index + 1]], index + 1, id_counter=id_counter
                )
        return tree

    # Option to remove background element because behave pushes it steps to all scenarios already
    if remove_background:
        for feature in json_file:
            if feature['elements'][0]['type'] == 'background':
                feature['elements'].pop(0)

    if remove_empty:
        for feature in json_file:
            # Create a working list
            scenarios = []

            # For each scenario in the feature
            for scenario in feature['elements']:
                # Add the scenario only if there are steps
                if len(scenario['steps']) > 0:
                    scenarios.append(scenario)

            # Replace the existing list with the working list
            feature['elements'] = scenarios

    if deduplicate:
        def check_dupe(current_feature, current_scenario, previous_scenario):
            if "autoretry" not in current_feature['tags'] and "autoretry" not in current_scenario['tags']:
                return False
            if previous_scenario['keyword'] != current_scenario['keyword']:
                return False
            elif previous_scenario['location'] != current_scenario['location']:
                return False
            elif previous_scenario['name'] != current_scenario['name']:
                return False
            elif previous_scenario['tags'] != current_scenario['tags']:
                return False
            elif previous_scenario['type'] != current_scenario['type']:
                return False
            else:
                return True

        for feature in json_file:
            # Create a working list
            scenarios = []

            # For each scenario in the feature
            for scenario in feature['elements']:
                # Append the scenario to the working list
                scenarios.append(scenario)

                # Check the previous scenario
                try:
                    # See if the previous scenario exists and matches
                    previous_scenario = scenarios[-2]
                    if check_dupe(feature, scenario, previous_scenario):
                        # Remove the earlier scenario from the working list
                        scenarios.pop(-2)
                except IndexError:
                    # If we're at the beginning of the list, don't do anything
                    pass

            # Replace the existing list with the working list
            feature['elements'] = scenarios

    # Begin the recursion
    return format_level(json_file)
