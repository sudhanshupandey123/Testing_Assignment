Feature: Company Details

  Scenario: Fetching Company Details
    Given He Opened Google Page
    When He Search Company Name "Actualize Consulting Engineers"
    When He Save Details Of Company
    Then He Make Csv File Of That

  Scenario Outline: Details Of Company
    Given He Opened Google Page
    When He Search Company Name "<company_name>"
    When He Save Details Of Company
    Then He Make Csv File Of That
    Examples:
      | company_name               |
      | Tech Mahindra              |
      | g7cr                       |
      | Fime India Private Limited |
      | TCS                        |