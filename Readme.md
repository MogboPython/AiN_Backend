# AiN Backend Services

This is a FastAPI application that handles form submissions for various registrations. It includes endpoints for health checks, email submissions, recruitment registrations, and conference signups. The application integrates with Google Sheets for data storage and utilizes asynchronous email sending functionality.

## Features

- Health Check: A simple endpoint to check the status of the API.
- Email Submission: Allows users to submit their email for AIESEC newsletters or updates.
- Recruitment Registration: Endpoint for users to register for recruitment, including detailed personal and academic information.
- Conference Signups: Specifically designed for conference registrations, capturing comprehensive attendee information.

## Installation

To run this project, you will need Python 3.8 or later. Follow these steps to set up the project environment:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:
`pip install -r requirements.txt`

## Usage

To start the FastAPI server, run the following command in the terminal:
`uvicorn main:app --reload`

This will start the server on `http://127.0.0.1:8000`. You can access the API documentation and test the endpoints by navigating to `http://127.0.0.1:8000/docs` in your web browser.

## Endpoints

- GET /api/healthcheck: Returns the status of the API.
- POST /api/submit_email: Endpoint to submit an email. Requires a JSON body with an email field.
- POST /api/recruitment: Registers a user for recruitment. Requires a JSON body with recruitment information.

## Configuration

The application requires access to Google Sheets for data storage. Ensure you have set up the Google Sheets API and have the necessary credentials in a credentials.json file in the project root.

## Contributing

Contributions to this project are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear commit messages.
4. Push your changes to the branch.
5. Submit a pull request.
