Feature: Amazon Cart

  Scenario: Amazon Cart Review
    Given User is on Amazon Page
    When He Search For Product Name "Dell Laptop"
    And He filters product based on more than "4" star rating
    And He add first "2" product to cart
    Then the cart value should be sum of products

  Scenario Outline: Amazon Cart With Different Product
    Given User is on Amazon Page
    When He Search For Product Name "<product>"
    And He filters product based on more than "<rating_star>" star rating
    And He add first "<num_of_prod>" product to cart
    Then the cart value should be sum of products
    Examples:

      | product            | rating_star | num_of_prod |
      | Lenovo Laptop      | 2.5         | 2           |
      | HP    Laptop       | 3.5         | 1           |
      | Redmi Mobile Phone | 4           | 5           |
