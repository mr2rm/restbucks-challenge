# Django Restbucks Challenage

An RESTful django development challenge for managing a small coffee shop

## Introduction 
In this challenge, you are going to develop a small django web application which manages 
restbucks coffee shop orders via REST APIs.

In restbucks, the manager can define variety of products via admin panel. Customers 
are able to order and customize their coffee with several options. Order can have a 
status: waiting, preparation, ready, delivered. Manager can chagne orders status. 
After each status change on order, you should notify the customer via email.

Here is sample catalog of products offered by restbucks:

Production > Customization option

- Latte >	Milk: skim, semi, whole
- Cappuccino > Size: small, medium, large
- Espresso > Shots: single, double, triple
- Tea
- Hot chocolate > Size: small, medium, large
- Cookie > Kind: chocolate chip, ginger
- All > Consume location: take away, in shop

For the sake of simplicity, consider each product has a constant price no matter which option is selected.

Note: UI is not important, you can use django admin UI.

The following REST APIs should be implemented and any customer should be able to consume the API 
using a secure way:

- View Menu (list of products)
- Order at coffee shop with options
- View his order (product list, pricing & order status)
- Change a waiting order
- Cancel a waiting orders

API response format is up to you.

This is a typical coffee shop problem which you're probably familiar with.
All defined requirements are just for testing your programming skills, they 
might not be meaningful in a real world example.

## Expectations

We want a clean, reusable, readable, and maintainable code with meaningful comments and docstrings.

## Estimation

After reading and understanding the challenge and all of expectations, estimate the required development time, send us your time cost estimation and your reasoning on how you've estimated 
this. **Do not start development before getting a confirmation from us**.

## Tests

- Write unit tests for your code with good coverage

## Task

1. Fork this repository (if you don't know how to do that, Google is your friend)
2. Develop the given challenge using django 1.8 or higher
3. Commit and Push your code to your new repository
4. Send us a pull request, we will review your code and get back to you
5. Try to enjoy this little challenge
