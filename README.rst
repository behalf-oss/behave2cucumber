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

For any questions or suggestions you can contact the authoers listed below.

Authors:
Andrey Goldgamer - andrey.goldgamer@behalf.com
Zvika Messing - zvika@behalf.com
