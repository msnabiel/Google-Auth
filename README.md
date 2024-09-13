# Google Login App

This is a simple web application built using Flask that allows users to log in using their Google account via OAuth 2.0. The application demonstrates the implementation of Google Sign-In, protecting routes that require authentication, and handling user sessions.

## Features

- Google OAuth 2.0 Authentication
- Protected routes that require users to log in
- Session management with Flask
- Proper logout functionality, including revoking Google credentials

## Prerequisites

- Python 3.7+
- Google Cloud Platform account for setting up OAuth 2.0 credentials
- Flask and required dependencies

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/google-Auth.git
   cd google-Auth
   ```

2. **Set Up a Google Cloud Project**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Navigate to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **OAuth 2.0 Client IDs**.
   - Set the application type to **Web application**.
   - Add `http://localhost:8501` to **Authorized JavaScript origins**.
   - Add `http://localhost:8501/auth` to **Authorized redirect URIs**.
   - Download the `client_secret.json` file and place it in the root directory of the project.

3. **Install Dependencies**

   Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   - Ensure that `client_secret.json` is correctly placed in the project directory.
   - Set `OAUTHLIB_INSECURE_TRANSPORT` to `1` to allow non-HTTPS traffic for development:

     ```bash
     export OAUTHLIB_INSECURE_TRANSPORT=1
     ```

5. **Run the Application**

   Start the Flask application:

   ```bash
   python main.py
   ```

   The application will run on [http://localhost:8501](http://localhost:8501).

## Usage

- **Login**: Go to the home page and click on the **Login** button to authenticate via Google.
- **Protected Area**: Access the protected area by navigating to `/protected_area`. This will only be accessible after logging in.
- **Logout**: Click on the **Logout** button to clear the session and revoke Google credentials.

## Troubleshooting

- **Port Already in Use**: If you encounter an error indicating that the address is already in use, ensure no other processes are using port 8501. You can change the port in the `app.run()` command if necessary.
  
- **Redirect URI Mismatch**: Ensure that the redirect URI in Google Cloud Console matches exactly with `http://localhost:8501/auth`.
  
- **Automatic Login After Logout**: To avoid automatic login after logout, make sure the Google credentials are properly revoked in the `/logout` route.

## Security Note

This application is for development purposes. Do not use the provided secret key in production. Replace it with a secure, random key for production deployments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or issues, please contact [msyednabiel@gmail.com](mailto:msyednabiel@gmail.com).

```
