# NB_UI_Test
## Directory Structure
```
|____Readme.md                      //help
|____allure-report                  //The report of results
|____data                           //The data for testing is stored
|____image                          //Store images for comparison.
|____tests                          //Test scripts folder by product
    |____   Web                     //Environment 001
            |____ Base.py           //Managing its setup and teardown for tests
            |____ Elements.py       //Store functions for clicking and other related features
            |____ test_xxx.py       //Test script
|____pytest.ini                     //Pytest setting configuration
|____requirements                   //Pip install library
```

---

## Python Version
`Python = 3.9.6`

---

## Install Library before test
`pip3 install -r requirements.txt`

---

## Run Test Command Line
`python3 -m pytest`

---

## Allure Report 
`--alluredir=./result`


## TestReport To Html (allure Report)
`allure generate ./result --clean`

