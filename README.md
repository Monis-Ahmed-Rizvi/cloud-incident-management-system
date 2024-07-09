# Cloud Incident Management System

## Project Overview

The Cloud Incident Management System is a Flask-based web application designed to help teams manage and track incidents related to cloud services. While it currently focuses on AWS, it provides a user-friendly interface for reporting incidents, viewing cloud resources, and managing user roles, with potential for expansion to other cloud platforms.

## Features

- User Authentication: Secure login and registration system.
- Role-Based Access Control: Different access levels for users and administrators.
- Incident Reporting: Users can report and track cloud-related incidents.
- AWS Resource Management: View and update AWS EC2 instance information.
- Admin Dashboard: Administrators can manage users and view all incidents.
- Chat Support: Integrated chatbot for user assistance.

## Technologies Used

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login for user session management
- Flask-WTF for form handling
- Flask-Migrate for database migrations
- Bootstrap for frontend styling
- AWS Boto3 for AWS integration
- OpenAI API for chatbot functionality

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/cloud-incident-management-system.git
   cd cloud-incident-management-system
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///app.db
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   python run.py
   ```

## Usage

1. Register a new user account.
2. Log in to the system.
3. Use the navigation bar to access different features:
   - Report a new incident
   - View existing incidents
   - Check cloud resources
   - Access the admin dashboard (for admin users)

## Contributing

Contributions to improve the Cloud Incident Management System are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Monis Ahmed Rizvi - [monisahmedrizvi@gmail.com](mailto:monisahmedrizvi@gmail.com)

Project Link: [https://github.com/Monis-Ahmed-Rizvi/cloud-incident-management-system](https://github.com/Monis-Ahmed-Rizvi/cloud-incident-management-system)