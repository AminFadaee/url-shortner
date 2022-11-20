# URL-Shortner
This project is the RESTful API of a url shortning system, written using:
* Python
* Flask
* PostgreSQL
* Redis
* Celery + RabbitMQ

## Features
Here is a list of features in this project:
1. Authentication system using Bearer Token
2. Ability to create short URLs and using them to redirect to the original URL
3. User specific custom representations for short URLs.
4. Analytics

## Documentation
The API swagger documentation can be found [here](api.yaml).
## Future
Currently the analytics is as basic as reporting the total views of a url.
I hope to extend this to more detailed analytic features.


## Author
Amin Fadaee
