# Blood Connect - Blood Bank Management System

Blood Connect is a robust blood bank management system developed using Flask for the backend, PostgreSQL as the database, and HTML, CSS, and JS for the frontend.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Adhithya-Laxman/Blood_bank.git
   cd Blood_bank
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   - Create a PostgreSQL database and update the configuration in `config.py`.
   - Apply migrations:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

4. **Run the Application:**
   ```bash
   python run.py
   ```

5. **Access the Application:**
   Open your web browser and navigate to `http://localhost:8080`.

## Features

- **Perfect Inventory Management:**
  Achieve optimal control and tracking of blood inventory with an advanced database system.

- **User-Friendly Interface:**
  Experience a visually appealing and intuitive UI designed to enhance productivity and user satisfaction.

- **Secure Login System:**
  Protect sensitive data and ensure confidentiality through a robust login mechanism.

- **Flask-Powered Backend:**
  Leverage the flexibility and scalability of Flask, a Python web framework, ensuring a reliable and future-proof solution.

## Routing and Controller Functions

- **Home:**
  - `/`: Displays the home page with information on available blood groups.

- **User Authentication:**
  - `/login`: Allows users to log in securely.
  - `/logout`: Logs out the current user.

- **About Us:**
  - `/about`: Displays information about the Blood Connect project.

- **Blood Search:**
  - `/<username>/blood_search`: Enables users to search for available blood units.

- **Place Request:**
  - `/<username>/blood_search/<hid>/<bid>`: Facilitates users in placing a request for blood units.

- **Donate Blood:**
  - `/<username>/donate`: Provides a form for users to donate blood.

- **Dashboard:**
  - `/<username>/dashboard`: Displays the user's dashboard with relevant information.

- **Previous Requests and Donations:**
  - `/<username>/your_requests`: Shows the user's previous blood requests.
  - `/<username>/your_donations`: Displays the user's history of blood donations.

- **User Signup:**
  - `/signup`: Allows new users to sign up for Blood Connect.

## Contributors

- [Adhithya Laxman R G]


---

Feel free to contribute to the project or report any issues. Happy coding!
