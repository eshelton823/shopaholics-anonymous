[![Build Status](https://travis-ci.com/uva-cs3240-f19/project-102-shopaholics-anonymous-project.svg?token=pyQDwdxMaHxzptDxnTDV&branch=master)](https://travis-ci.com/uva-cs3240-f19/project-102-shopaholics-anonymous-project)
### Shopaholics Anonymous presents...

# Shopper Share
## Welcome to our shopper share website! 

#### Heroku URL: https://shopaholics-anonymous.herokuapp.com
#### The Team: Lukas Curtis, Makenna Page, Jason Ashley, Richard Park, Elizabeth Shelton

### Here's a typical flow of how our website works:
1. Sign up and sign in with either Google or a unique username and password
2. Choose whether to act as a customer or a driver
3. View your information on the Dashboard
#### If you're a customer...
1. Create a grocery list of items and specify dropoff time and location
2. Pay for your list using Stripe (see test information below)
3. Your order will be matched with an available driver 
4. Chat with your driver via instant messaging on your Dashboard
5. Once you've received your order, resolve it from the Dashboard to free yourself and the driver for a new purchase
6. View past orders by clicking on their ID at the bottom of your Dashboard

#### If you're a driver...
1. Access your Driver Dashboard for the first time to fill out your driver-specific information
2. Click on Start Matching to make yourself available to match with an order
3. Once you're matched with an order, you can see the grocery list, dropoff location, and delivery instructions on your Driver Dashboard
4. Chat with your customer via instant messaging on your Driver Dashboard
5. Once your customer has resolved the order, you can choose to start matching again
6. View past completed orders by clicking on their ID at the bottom of your Driver Dashboard
7. See your total money earned and deliveries made on the Driver Dashboard


#### Sign Up Information
* If you sign up with your own unique credentials instead of using Google, you must use a valid email to be able to reset your password via email 
  * Otherwise, we use Google's OAuth to create a new account and sign in
  * You cannot sign up with Google and then access that account with a normal sign in or vice versa
* You only fill out general user information on sign up. If you wish to be a driver, you will need to fill out additional info by accessing the Driver Dashboard

#### Payment Information
* We use Stripe as our payment system (https://stripe.com/). Stripe only accepts valid credit card info. To use test information:
  * Email: Any valid email pattern
  * Credit Card Number: 4242 4242 4242 4242
  * Expiration: Any month and year in the future (e.g. 02/2020)
  * CVV: Any three-digit number
  
#### Chat Information
Our chat functionality uses Twilio (https://www.twilio.com/)

#### Store Information
Our search results are from Walmart (https://www.walmart.com/)

#### Other Notable Features
* Security
  * You cannot access the store page until you are logged in
  * You cannot access the sign up or sign in pages once logged in
  * URLs do not change with the user, so you cannot access someone else's information by typing in a certain URL
  * You cannot access an order summary of which you were neither the customer nor the driver
* Google maps and addressing
  * When you create an order and fill out dropoff, Google will auto-populate the address field based on what you type
  * If you are the driver, you can see a map of dropoff location from the Driver Dashboard
  * You can see a map of dropoff location when viewing a past order (either as a user or a driver)
  
