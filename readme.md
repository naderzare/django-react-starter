# Django React Starter Project

Django React Starter Project is a boilerplate repository for building full-stack web applications using Django as the backend framework and React as the frontend. It provides a straightforward setup for modern web app development, supporting either separate or unified deployment of the backend and frontend.

## Why This Project Is Important

- **Quick Start**: Offers a ready-to-use structure for full-stack projects, reducing setup and boilerplate.
- **Flexibility**: Lets you run the backend and frontend separately during development or serve the React build via Django in production.
- **Scalability**: Follows best practices to make extending and scaling easier.
- **Developer-Friendly**: Includes features like CORS support and environment-based configuration.

## Features

- **Backend**: Django-powered REST API (via Django REST Framework).
- **Frontend**: React application (can use Bootstrap or any other library for styling).
- **CORS Support**: Preconfigured support for cross-origin requests during local development.
- **Environment Variables**: Easily manage settings for development or production using .env.
- **Unified Deployment**: Option to serve the React build directly from Django.

## How to Run the Project

### Prerequisites

#### Backend Requirements:

- Python (3.9 or higher)
- Virtual environment setup (optional but recommended)

#### Frontend Requirements:

- Node.js (16.x or higher)
- npm or Yarn package manager

### Running the Backend (Django) Separately

#### Clone the Repository

```bash
git clone https://github.com/yourusername/django-react-starter.git
cd django-react-starter
```

#### Create and Activate a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Run Migrations

```bash
python manage.py migrate
```

#### Run the Django Server

```bash
python manage.py runserver
```

#### Access the Backend

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
If you’re using Django REST Framework, you can view your API endpoints or the DRF browsable API at various URLs (e.g., [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)).

### Running the Frontend (React) Separately

#### Navigate to the frontend Directory

```bash
cd frontend
```

#### Install Node.js Dependencies

```bash
npm install
```

#### Run the React Development Server

```bash
npm start
```

#### Access the Frontend

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Running the Backend and Frontend Together

To serve the React build through Django in production or a unified environment:

#### Build the React App

```bash
cd frontend
npm run build
```

This will generate a build folder inside `frontend/`.

#### Place or Copy the Build into Django’s Static/Template Directory

Move the contents of `build` into a folder recognized by Django for static files or templates (this can be automated via scripts).
Alternatively, configure your Django settings to serve the build folder directly (e.g., using WhiteNoise or custom static files settings).

#### Run the Django Server

```bash
python manage.py runserver
```

#### Access the Unified App

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). You should see the React frontend served by Django.
Any API routes (e.g., `/api/...`) will continue to be handled by Django views/DRF.

## Project Structure

Below is an example structure; your actual layout may vary:

```bash
django-react-starter/
├── manage.py               # Django management script
├── backend/                # Main Django project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                    # Example Django app for APIs
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── ...
├── frontend/
│   ├── build/                  # Production build of React
│   ├── public/
│   ├── src/
│   └── package.json
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

- `backend/`: Django project containing all backend logic, models, and API endpoints.
- `frontend/`: React project with source code (`src/`) and a production build folder (`build/`).

## API Endpoints

Below is an example of how your Django REST Framework endpoints might look. Adjust according to your actual implementation.

### Add a User

**POST** `/api/add`

#### Request Body:

```json
{
  "username": "john_doe",
  "age": 30
}
```

#### Response:

```json
{
  "id": 1,
  "message": "User created successfully"
}
```

### Get All Users

**GET** `/api/all`

#### Response:

```json
[
  {
    "id": 1,
    "username": "john_doe",
    "age": 30
  }
]
```

(These are just examples; you’ll configure URLs in your Django app’s `urls.py`.)

## Google Login Integration

- get google client id and client secret from google developer console
- add client id and client secret in .env file of django project
- add google client id to frontend .env file

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit and push your changes.
4. Open a pull request for review.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions or feedback, feel free to reach out or open an issue in the repository.

## Keywords

- Django React Starter
- Full-stack web development
- Django REST Framework
- React frontend with Django
- Modern web app example