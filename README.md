# Smart Realestate

Smart Realestate is a house price tracking and prediction system.

The system is service oriented with high scalability and cutting-edge technologies like Node.js/Express, PRC API, Python, web scraper, MongoDB and the most hot machine learning framework -- TensorFlow. 

There are four modules in the system.

- Front server: a dynamic search website constructed by Node.js, and return estimated price and search result list.
- API server: a RPC API service server written in Python, accepting request from front server and call TensorFlow service
- Data fetcher: a web crawler continously gather property information.
- Machine learning: a online prediction service and offline training model.

System Architecture
![Architecture](https://github.com/stevensshi/smart-realestate/Architecture.png)
