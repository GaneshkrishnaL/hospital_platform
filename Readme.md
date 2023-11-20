# Hospital Platform Project - README

## Overview
This Django-based project, Hospital Platform, is designed to manage hospital reservations. It includes features for user registration, hospital management, bed availability tracking, and reservation handling.

## Features
- User authentication and management
- Hospital and bed management
- Reservation system for patients
- Dashboard for patients and hospitals
- Bed status updates (Available, Occupied, Maintenance)

## Installation
1. Clone the repository.
2. Install Django and other dependencies (see `requirements.txt`).
3. Run `manage.py migrate` to set up the database.
4. Start the server with `manage.py runserver`.

## Usage
- **User Registration**: New users can sign up as patients or hospitals.
- **Login**: Users log in to access their respective dashboards.
- **Dashboard**: 
  - Patients view available hospitals and make reservations.
  - Hospitals manage bed availability and handle reservations.
- **Reservation**: Patients make reservations for available beds.

## Structure
- `models.py`: Defines User, Hospital, Bed, and Reservation models.
- `views.py`: Contains logic for handling requests and rendering responses.
- `templates`: HTML files for the user interface (not included in the listing).
