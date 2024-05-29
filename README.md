# Listing Project with FastAPI

## Introduction
This is a Listing project built using the FastAPI web framework. The project allows users to create an account, and each user can create, read, update, and delete their own listings.

## Features
- User authentication and authorization
- CRUD (Create, Read, Update, Delete) operations for listings
- Request validation
- Rate limiting (5 requests per minute)

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Redis (for rate limiting)

### Installation
1. Clone the repository: git clone https://github.com/your-username/listing-project.git

2. Change to the project directory: cd listing-project

3. Create a virtual environment and activate it: python -m venv .venv source .venv/bin/activate

4. Install the required dependencies: pip install -r requirements.txt

5. Set the environment variables: export DEFAULT_USER_PASSWORD=your-secure-password

6. Run the database migrations: alembic upgrade head

7. Start the development server: uvicorn config:app --host 0.0.0.0 --port 3000 --reload


The application should now be running at `http://localhost:3000`.

## Usage
1. Create a new user by sending a POST request to `/users/register`.
2. Authenticate the user by sending a POST request to `/users/login`.
3. Use the obtained access token to make requests to the listing endpoints, such as `/listings`.

## Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License
This project is licensed under the [MIT License](LICENSE).


