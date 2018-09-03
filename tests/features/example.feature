Feature: Feature example text

    Scenario Outline: Scenario example text
        Given user is on "homepage" page
        Then user goes to "<pages>" page

       Examples:
        | pages |
        | bing  |
        | yahoo |

    Scenario: Scenario Two example text
        Given user is on "homepage" page
        When user searches for "python"
        Then site "python.org" should be in results