# Confidentier first release

This is the source code for [Confidentier](www.confidentier.com).
A Platform

This repo contains as example how to use nicegui to implement 
1. Login
2. Payments (Stripe)
3. Google Firestore (Database)
4. AI Platform (OpenAI)
5. Landing page


## Project structure
 
- API  
    This contains endpoints from FastApi, in this case only the webhook one
- domain  
    This contains use cases for the project, mostly operations that will require some service like Upload files, OpenAI api or Database operations, all the business logic comes here
- models  
    Mostly Pydantic models used to send data in our application and parse from and to JSON
- pages  
    All nicegui components and pages are here.
- services  
    External services that does not belong to the app or business logic, it can be DB, AI apis, etc.

**main.py** is my entry point.  
**.envexample** contains the keys that our .env file will require  
**Dockerfile** is the image we build to deploy the app to some cloud  

## Setup locally

- You will need a descope account
- Stripe account also required
- run `pip install -r requirements.txt`
- start with `python main.py`
