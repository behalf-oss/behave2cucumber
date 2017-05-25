Behave to Cucumber formatter
============================

This project helps solving the incompatibilty of Behave's genereated json reports to tools using Cucumber json reports.
Its done by reformatting the Behave json to Cucumber json.
This script was developed during work on automation tools for Behalf inc. automation team.
The script was developed and tested on Python 2.7, you're welcome to use this script and format it to other python versions.

For easy install use: "pip install behave2cucumber"

Example of usage:
 .. code-block:: python

    import json
    import behave2cucumber
    with open('behave_json.json') as behave_json:
        cucumber_json = behave2cucumber.convert(json.load(behave_json))


Running from bash
-------------------------
Main has been added thanks to @lawnmowerlatte and now you can run:
 .. code-block:: bash
 
   python -m behave2cucumber


Running tests
-------------------------
To run tests: 
 .. code-block:: bash
    
    ./test_script
