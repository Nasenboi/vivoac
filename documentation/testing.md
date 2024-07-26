<!---         
    Hier kommt rein:
    Wie der code getestet wird!


      -->

# Testing

This chapter explains how the code is tested. Currently, only one form of tests are supported for this project: unit tests.


## Unit Tests

The unit tests verify the functionality of the backend code. The python start script is called [test-main.py](../test_main.py). This script will instantiate multiple test classes, each for a different api route. These test classes have multiple neat function, that each call upon an api endpoint with some test data and verify the results. These test classes can be found under _package/tests/*_.

### test-main.py

A few additional infos may help you to better understand the contents of the test-main.py script.
This script is built very similar to the default main.py script. That means, its main purpose is to launch in instance of the _api_engine_ class. 


### test base class