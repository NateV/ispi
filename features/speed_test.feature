
Feature: Downloading and Saving Speed information
    Scenario: Downloading and Saving Speed information
        Given I do a speed test that completes successfully
        And I save the information to a local database
        Then I can retrieve the information from the database
