# TripCase Migration Assistant

## Overview

The **TripCase Migration Assistant** is a Python-based tool designed to allow users to **download their cruise, flight, and hotel data** from the **TripCase** platform. ThisMigration Assistant enables users to extract their travel itineraries, including cruise details, flight information, and hotel bookings, and export them in **JSON format** for future use.

Once the new platform is live, you can **upload this data to the platform** to manage your travel plans more effectively. 

### **Important Notice**  
**TripCase will be shutting down on April 1, 2025.** After this date, the TripCase platform will no longer be available, and thisMigration Assistant will no longer function.

In the meantime, I am **actively working on building a new travel platform**. This platform will allow users to upload and manage their travel data, including the data you've downloaded using this Migration Assistant. The platform will provide a seamless experience for managing all your travel information in one place.

**Stay tuned for more details about the new platform!**

## Features

- **Cruise Data:** Download details about your cruise itineraries, such as cruise line, ship name, embarkation date, and port of call.
- **Flight Information:** Scrape flight numbers, departure times, arrival times, and statuses.
- **Hotel Bookings:** Extract hotel reservation details, including hotel name, location, and check-in/check-out dates.
- **Export Data in JSON Format:** The Migration Assistant exports all the extracted data in  for easy uploading and integration with the new platform.


## Installation

### Prerequisites

- Python 3.x
- Pip (Python package manager)

### Steps

1. **Clone this repository:**

``` bash
   git clone https://github.com/yourusername/tripcase-migration-assistant.git
   cd tripcase-migration-assistant
```

2. **Install required dependencies:**

```bash
pip install -r requirements.txt
```
3. Enter your credentials in the `temp.env` file and rename the `temp.env` file to `.env`

4. Run the python script

