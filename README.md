# Smart Realestate

Smart Realestate is a house price tracking and predicting system, which fetches property data from web, trains prediction model by TensorFlow and eventually give estimate price for given location.

The system is service oriented with high scalability and cutting-edge technologies like Node.js/Express, PRC API, Python, web scraper, MongoDB and the most hot machine learning framework -- TensorFlow. 

There are four modules in the system.

- Front server: a dynamic search website constructed by Node.js, and return estimated price and search result list.
- API server: a RPC API service server written in Python, accepting request from front server and call TensorFlow service.
- Machine learning: a online prediction service useing TensorFlow and offline training model.
- Data fetcher: a web crawler continously gather property information into MongoDB.

Code Structure:

| Folder  | Content |
| ------------- | ------------- |
| AMQP  | Message queue service (RabbitMQ)  |
| data_fether  | Python crawler (Scrapy)  |
| ml_service  | Prediction service and marchine learning (TensorFlow)  |
| Nodejs_server  | Front server (Node.js)  |
| rpc_service  | Remote procedure call service  |
| mongodb  | Mongoose |


System Architecture
![Architecture](https://raw.githubusercontent.com/stevensshi/smart-realestate/gh-pages/architecture.png)

The system is in prototyping and will be online during Chirstmas
