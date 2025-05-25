
# UCJayy Fashion Store

UCJayy Fashion Store is a web application that provides personalized fashion recommendations and allows users to browse and manage fashion items. It is built with a Django backend and a React frontend.

## Features
- User authentication (signup, login, logout)
- Personalized fashion recommendations
- Item browsing and management
- Responsive user interface

## Prerequisites
- Python 3.11 or higher
- Node.js and npm (for the frontend)
- pip (Python package manager)

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
5. The backend will be available at `http://127.0.0.1:8000/`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required npm packages:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```
4. The frontend will be available at `http://localhost:3000/`.

## Usage
1. Open the frontend in your browser at `http://localhost:3000/`.
2. Register or log in to access personalized recommendations and browse items.

## Media and Static Files
- Fashion item images are stored in the `backend/media/fashion_images/` directory.
- Static files for the frontend are located in the `frontend/public/` directory.

## Future Enhancements
- Add advanced recommendation algorithms.
- Implement a cart and checkout system.
- Enhance the UI with Material-UI or Bootstrap.

## License
This project is licensed under the MIT License.
```

Let me know if you need further adjustments or additional sections!
