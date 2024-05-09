### DDD-fastapi-auth

This is a pet project aimed at exploring Domain-Driven Design (DDD) architecture with FastAPI for building web applications.

#### Technologies Used

- **Python**: ^3.11
- **FastAPI**: ^0.111.0
- **SQLAlchemy**: ^2.0.30
- **asyncpg**: ^0.29.0
- **pre-commit**: ^3.7.0
- **uvicorn**: {extras = ["all"], version = "^0.29.0"}


#### Project Structure Description

- **app**: Root directory of the project.
- **application**: Contains the application layer of the project.
  - **api**: Contains FastAPI endpoints and routing logic.
- **domain**: Contains domain-specific entities, value objects, and domain services.
- **infrastructure**: Contains implementations of infrastructure-related components such as databases, external services, etc.
- **logic**: Contains business logic of the application.



#### Getting Started

1. Clone this repository.
2. Navigate to the project directory.
3. Create a virtual environment using Python 3.11 with `poetry shell`.
4. Install dependencies using `poetry install`.
5. Set up environment variables using `.env.example` as a template.
6. Run the application using `uvicorn --factory app.application.api.main:create_app --reload`.

Feel free to explore and modify the project as needed for your own purposes!
