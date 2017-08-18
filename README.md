### Status
[![Build Status](https://travis-ci.org/keyprqa/GitHubAPI.svg?branch=master)](https://travis-ci.org/keyprqa/GitHubAPI)

# TestRepo
**It's Python GitHub API tests.**

There presented 2 type of tests:
    `BDD Behave`
    `PyTest`
    
Run Tests local:     
* Install git:
    > brew install git
    
* Next step - install python:
    > brew install python 
    
* Install python virtualenv: 
    > sudo pip install virtualenv
    
* Create virtual environment for mes-backend-automation:
    > virtualenv env

* Activate virtual environment:
    > source env/bin/activate
    
* Clone GitHubAPI repository with ssh ( need configure two factor authorisation and add ssh public key to git hub repository) :
    > git clone https://github.com/keyprqa/GitHubAPI.git

* Navigate to project folder and install requirements :
    > pip install -r requirements.txt
    
* Run PyTest tests :
    > py.test -v py_test/

* Run BDD test :
    > behave bdd_tests/
    

Tests connected to CI Travis and could be running there:
   > https://travis-ci.org/keyprqa/GitHubAPI


