Hamehir Lamishtaken Apartment Notifier

Welcome to the Hamehir Lamishtaken Apartment Notifier GitHub repository! This project showcases a Lambda function coded in Python that plays a crucial role in keeping you updated about new apartment releases from previous projects at attractive prices on the "Hamehir Lamishtaken" website in Israel. The function accomplishes this by notifying you via both WhatsApp and email, ensuring you never miss out on a great opportunity.

Project Overview
The primary objective of this project is to ensure you're promptly informed about new apartment releases that match your preferences. To achieve this, the Lambda function scans the "Hamehir Lamishtaken" website regularly. It then evaluates whether a newly listed apartment is worth your consideration based on predefined criteria, such as the price and location.

Key Features
Website Scanning: The Lambda function actively scans the "Hamehir Lamishtaken" website to identify new apartment listings.

Real-time Notifications: Upon discovering a new apartment, the function sends real-time notifications to your WhatsApp and email, providing you with crucial information.

Smart Filtering: The function maintains a JSON file within AWS S3 storage. This file stores information about previously identified apartments, allowing the function to filter out duplicates. Furthermore, if an apartment becomes vacant in an area you already have data for, the function will only notify you if the price is more attractive than what you already know.

Technologies and Services Used
Twilio: Integration with Twilio enables the function to send WhatsApp messages, ensuring you receive timely notifications.

Google SMTP: Google's SMTP service is employed to send email notifications, offering you multiple channels of communication.

boto3: This Python library facilitates seamless interaction with AWS storage services, ensuring efficient management of the JSON data.

Getting Started
To set up the project locally and adapt it to your needs, follow these steps:

Clone the repository: git clone https://github.com/your-username/hamehir-lamishtaken-notifier.git
Configure your Twilio account credentials in twilio_config.json.
Set up your Google SMTP credentials for sending emails in email_config.json.
Install the required Python dependencies.
Customize the function's logic and filtering criteria as per your preferences.
Deploy the Lambda function to your AWS account.
Set up a schedule for running the Lambda function at desired intervals.
Contact Information
For any questions, clarifications, or further explanations about the project, feel free to contact me privately. I'd be more than happy to assist you!

Name: Afik Peretz
Email: afikperetz5235@gmail.com
Let's stay connected and stay ahead in the apartment hunting game! 🏢🔍




