# Planning Calculator

This repository contains a Python script that utilizes the Google Calendar API to calculate the total number of free hours between specific hours each day over a given timeframe. This can be useful for planning and scheduling purposes.

## Getting Started

To use this script, follow the steps below:

### 1. Set Up Google Calendar API

- Go to the [Google Developers Console](https://console.developers.google.com/).
- Create a new project.
- Enable the Google Calendar API for your project.
- Create credentials (OAuth 2.0 client ID) and download the `credentials.json` file.

### 2. Install Required Python Packages

You'll need the following Python packages: `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`, and `datetime`. Install them using pip:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 3. Write the Python Script

Refer to the `script.py` file in this repository for an example script that syncs with your Google Calendar, pulls the free times between a specified start and end time each day, and calculates the total number of free hours over a given timeframe.

### 4. Script Explanation

You can modify the `start_hour`, `end_hour`, and `days` variables in the `main()` function to match your requirements.

### 5. Run the Script

Ensure your `credentials.json` file is in the same directory as the script. Run the script, and it will output the free hours per day and the total free hours over the specified timeframe.

## Customization

Feel free to customize the script based on your specific needs. For example, you can exclude weekends or handle multiple calendars.

## License

This project is licensed under the [MIT License](LICENSE).
