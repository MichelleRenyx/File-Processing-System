# Intelligent Form File Processor
**Author:** Yuxin Ren

**Contact:** micheren1@outlook.com

***Note: This project is still under development. You are only authorized to read and use it when you receive the link. Please do not share it with others. Thank you.***

---
**Visit the Deployed Version at:**

http://ec2-3-27-59-112.ap-southeast-2.compute.amazonaws.com/
- **IMPORTANT**: This version is only used to demonstrate the developed results and functions. Please DO NOT use it for large-scale testing to avoid overloading the external platform like OpenAI API and AWS EC2 and causing inaccurate results.

**Demonstration Video:**

https://youtu.be/2n-eY0MsGiA

## Description
This project is a file processing system developed with Django and React and hosted in Docker containers, using OpenAI's API for data processing, AWS S3 for static file storage and AWS EC2 for deployment. The system enables users to process uploaded .xlsx and .csv files by providing natural language input, and the processed files can be downloaded as .csv.

- The first view of the web, providing a introduction and an entrance for file uploading.
![FirstView](/firstview.png)

- When proper type file is uploaded, the system provides a preview of current file.
![FileUploadedView](/fileuploaded.png)

- Input the identify patterns using netrual language. (e.g. "Find email addresses in the Email column and replace
them with 'REDACTED'.") Click Button 'Process Data'.
![ProcessedView](/processed.png)

- If the preview of processed file meets your expectations, you can click the Button ‘Download Processed Data’ to download it as .csv format.

## Features
- File upload, preview and management through Django.
- Integration with OpenAI API for advanced natural language processing.
- RESTful API endpoints to interact with the frontend.
- Use Tailwind and React for better frontend visual effects.
- Set up Jest for Unit Test and use GitHub Actions for CI/CD.
- Deployed using Docker, AWS EC2
- Storage of static files in AWS S3.
- Secure handling of secrets using GitHub Secrets.

## Tech Stack
- **Backend:** Django, Python3.12, OpenAI API
- **Frontend Interaction:** React, Javascript, Tailwind, CSS
- **Deployment:** Docker, GitHub Actions for CI/CD, AWS EC2
- **Tools:** Postman, AWS S3, Vite

## Installation
### Prerequisites
Make sure you have the following software installed on your machine:
- Python (Python 3.12 is recommended)
- Node.js (Node.js 18 is recommended)
- npm (usually installed with Node.js)
- Docker (if you plan to run your application in containers)
### Step 1
Clone the repository to your local machine:
```bash
git clone https://github.com/MichelleRenyx/File-Processing-System.git

cd <your-repository>
```
To run the project locally, you need to set up the environment variables. Create a .env file in the root directory of the backend/fileprocessor and add the following:
- /backend/fileprocessor/.env
```env
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
```
- /frontend/.env
```env
VITE_API_URL="http://localhost:8000"
```
### Step 2
Enter the backend directory, install dependencies and build backend resources:
```bash
python3 -m venv env

source env/bin/activate
```
```bash
cd backend/fileprocessor

pip install -r requirements.txt

python3 manage.py migrate
```
If there's no error after 'migrate' step,
```bash
python3 manage.py runserver
```
### Step 3
Enter the frontend directory, install dependencies and build frontend resources:
```bash
# make sure you are in the (env)

cd frontend

npm install

npm run dev
```
Then you are supposed to visit the Web with the guide of Vite.

## Future Improvements
* **Handling Large Files:** To manage large file uploads better, we're considering using load balancers like Nginx. This would help spread upload requests across several servers. We also want to use techniques like streaming and chunking to keep memory use low and avoid server crashes.

* **Upload File Enhancements:** The file format and content check before processing is neccesary to guard against malicious uploads. This includes implementing strict sanitization protocols to ensure the files are safe and do not contain any harmful data.

* **Complete Unit Tests:** Due to time constraints, I only implemented 2 unit tests (DataProcessor and DownloadComponent) as example. Moving forward, the system needs a more systematic and comprehensive set of test files to ensure security and robustness.

* **Improved Container/API Strategy:** The deployment version of this project currently employs a low-cost Open API strategy and a free EC2 tier. For future enterprise-level development, we need to consider strategies that are closer to production standards.

* **Domain Name Binding:** The website is currently accessible through the AWS Instance's IPv4 DNS. In the future, it need to be bind to a private domain name for better commercialization.

## Reference
- Tech With Tim. "Django & React Web App Tutorial - Authentication, Databases, Deployment & More." YouTube, https://www.youtube.com/watch?v=c-QsfbznSXI.

- CodeWithAamir. "React CSV Download." YouTube, https://www.youtube.com/watch?v=IPEqb_AJbAQ.

- Super Coders. "Deploying Django and React on AWS with Docker and GitHub Actions CI CD Pipeline | Amazon Clone 16." YouTube, https://www.youtube.com/watch?v=QHCsaG9dLI4.

- Stack Overflow. "Stylesheet not loaded because of MIME-type." https://stackoverflow.com/questions/48248832/stylesheet-not-loaded-because-of-mime-type.




---