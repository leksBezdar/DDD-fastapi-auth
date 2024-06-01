### DDD-fastapi-auth

This pet project was made to demonstrate the DDD architecture within the authorization service with FastAPI and aiokafka.


#### Key python libs

- **FastAPI**: Async web framework
- **SQLAlchemy**: ORM
- **punq**: DI tool
- **pytest**: Testing framework

#### Infrastructure
- **MongoDB**: NoSQL database
- **motor**: Async engine for MongoDB
- **aiokafka**: Distributed event streaming platform
- **redis**: Caching database


#### Getting Started

1. Clone this repository.
2. Use `Make all` to setup and build the docker containers.
3. Use `Make app-logs` to track logs in real time.
4. Use `Make app-down` to stop the application.

Feel free to explore and modify the project as needed for your own purposes!
