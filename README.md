# Parsing Challenge

This service is designed to efficiently process and import product data 
from a large XML file into a PostgreSQL database. It handles large datasets 
by streaming the data, ensuring that it does not overload system memory. 
The service is containerized with Docker, making it easy to deploy and scale.

## Features

- **Efficient Data Processing**: Uses `lxml.etree.iterparse` for memory-efficient parsing of large XML files.
- **Dockerized**: Both the application and the PostgreSQL database run in Docker containers.
- **Database Integration**: Automatically sets up the database schema upon startup.
- **Code Quality**: Integrates pre-commit hooks for code formatting and linting.

## Prerequisites

- Docker
- Docker Compose
- Git (for cloning the repository)

## Installation

1. **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2. **Environment Setup:**

    Copy the example environment file to create your own environment variables file:

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file to suit your environment settings like database credentials.

3. **Build and Run with Docker Compose:**

    Use Docker Compose to build and run the services defined in the `docker-compose.yml` file:

    ```bash
    docker compose up --build -d
    ```

    This command will start all the required services in detached mode.

## Usage

Once the services are running, the product importer will begin processing 
the XML file specified in the `.env` file. The data will be inserted into 
the PostgreSQL database.

## Stopping the Service

To stop all services, use the following Docker Compose command:

   ```bash
   docker compose down -v
   ```

## Thanks for Visiting!
