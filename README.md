# Web-ARegex-Pattern-Matching-and-Replacement
Web Application for Regex Pattern Matching and Replacement

- What is the project doing


Save the processed data on AWS cloud as .csv file with 1 day lifecycle, users can downnload the processed csv file from the cloud.

- Startup environment
- Backend/frontend



- (for Production Ready Standerd:)

.env -> .env.sample

Unit tests (Notes: Unit test is incomplete? Potential problems? Areas for improvement)

--- 
TODO
* Redis for better speed?
* Frontend UI using Tailwind?
* npl algorithm?
--- 
Future Improvements
* Upload File Improvements: Before processing any files, verify their format and content to prevent malicious uploads. Implement stringent sanitization protocols to ensure the files do not contain any harmful data.

* Handling Large Files: Utilize load balancers like Nginx to distribute incoming file upload requests across multiple server instances. Employ streaming and chunking techniques to minimize memory usage and reduce the risk of server crashes.

---
Reference
- Django & React Web App Tutorial - Authentication, Databases, Deployment & More... \ https://www.youtube.com/watch?v=c-QsfbznSXI \ author: Tech With Tim

- React CSV Download \ https://www.youtube.com/watch?v=IPEqb_AJbAQ \ author: CodeWithAamir

---