Behave to Cucumber formatter
============================

This project helps solving the incompatibilty of Behave's genereated json reports to tools using Cucumber json reports.
Its done by reformatting the Behave json to Cucumber json.
This script was developed during work on automation tools for Behalf inc. automation team.
The script was developed and tested on Python 2.7, you're welcome to use this script and format it to other python versions.

For easy install use: "pip install b2c"

Example of usage:
 .. code-block:: python

    import json
    import b2c
    with open('behave_json.json') as behave_json:
        cucumber_json = b2c.convert(json.load(behave_json))

There is a list of know issue: https://github.com/behalfinc/b2c/issues/2

For any questions or suggestions you can contact the authors listed below.

Running tests
-------------------------
To run tests: 
 .. code-block:: bash
    
    ./test_script

Authors:
Andrey Goldgamer - andrey.goldgamer@behalf.com
Zvika Messing - zvika@behalf.com
