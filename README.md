# Web-File-Processing-System

Visit the Deployed Version at http://ec2-3-27-59-112.ap-southeast-2.compute.amazonaws.com/
- IMPORTANT: This version is only used to demonstrate the developed results and functions. Please do not use it for large-scale testing to avoid overloading the external platform like OpenAI API and AWS EC2 and causing inaccurate results.
## Description
This project is a file processing system developed with Django and React and hosted in Docker containers. It leverages OpenAI's API for data processing and AWS S3 for static file storage. The system enables users to process uploaded .xlsx and .csv files by providing natural language input, and users can download the processed file as .csv.

## Features
- File upload and management through Django.
- Integration with OpenAI API for advanced natural language processing.
- Storage of static files in AWS S3.
- RESTful API endpoints to interact with the frontend.
- Secure handling of secrets using GitHub Secrets and environment variables in Docker.

## Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite (development), Extendable to other databases as per requirements
- **Frontend Interaction:** React (handled separately)
- **API Testing:** Postman or any other API testing tool
- **Deployment:** Docker, GitHub Actions for CI/CD, AWS EC2
- **Security:** Managed through environment variables and GitHub Secrets

## Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/your-github-username/backend-fileprocessor.git
cd backend-fileprocessor

To run the project locally, you need to set up the environment variables. Create a .env file in the root directory of the project and add the following:

OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name

Save the processed data on AWS cloud as .csv file with 1 day lifecycle, users can downnload the processed csv file from the cloud by clicking the button.

- Startup environment
- Backend/frontend

- Frontend UI using Tailwind

- Call OpenAI API for natural language processing

- (for Production Ready Standerd:)

.env -> .env.sample

Unit tests (Notes: Unit test is incomplete? Potential problems? Areas for improvement)
Due to time, only DataProcessor, DownloadComponent...
--- 
TODO
* Unit tests + CI/CD

--- 
Future Improvements
* Upload File Improvements: Before processing any files, verify their format and content to prevent malicious uploads. Implement stringent sanitization protocols to ensure the files do not contain any harmful data.

* Handling Large Files: Utilize load balancers like Nginx to distribute incoming file upload requests across multiple server instances. Employ streaming and chunking techniques to minimize memory usage and reduce the risk of server crashes.

---
Reference
- Django & React Web App Tutorial - Authentication, Databases, Deployment & More... \ https://www.youtube.com/watch?v=c-QsfbznSXI \ author: Tech With Tim

- React CSV Download \ https://www.youtube.com/watch?v=IPEqb_AJbAQ \ author: CodeWithAamir

---