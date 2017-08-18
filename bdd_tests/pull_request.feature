# Created by alexandrpolishchuk at 7/16/17
Feature: Pull Request
  # Enter feature description here

  Scenario: Create Pull Requests
    Given we check count of active pull requests
    Then we create new pull requests
    Then we check count of pull requests increased for 1
    And we delete created pull request
