# TikTasks

Presented by	Thorung Boonkaew 6510545454

## Project Overview

**TikTasks** is a web-based to-do application built with Django for the backend and HTML/CSS/JavaScript for the frontend. It allows users to manage their daily tasks with a simple, clean interface. Users can register, log in, add tasks, track progress, and manage their to-do list effectively. The app also supports optional image uploads.

## Features

1. User Authentication

    * Users can create an account (Signup) and log in (Login) to access their to-do list.

2. View Todo List

    * After logging in, users can see all their to-do items. The app queries tasks from the Neon PostgreSQL database and displays them dynamically.

3. Add New Todo Items

    * Users can add new tasks using a form and upload an image. The new task is saved to the database and appears in the task list.

4. Update Task Status

    * Each task can be updated to reflect its current status (e.g., "In Progress", "Done"). This helps users track their progress easily.

5. Edit Task detail

    * Users can edit the title, description. This feature allows updates to task details without deleting and re-adding them.

6. Delete Todo Items

    * Users can remove tasks from their list. The selected task is deleted from the database permanently.

## Framework

### Frontend

* **HTML** (HyperText Markup Language) is used to structure the content on the webpage.
* **CSS** (Cascading Style Sheets) is used to style the webpage, for example, colors, layouts, and fonts.

* **JavaScript** helps add interactivity, like clicking buttons to update tasks without refreshing the page.

    Since this project is small and beginner-friendly, basic HTML/CSS/JavaScript is enough and easier to manage.

### Backend

* **Django** is beginner-friendly and comes with many built-in features like user authentication, an admin panel, and database models.
* It uses Python, which is easy to read and understand.
* Django helps me handle server-side logic such as user login, adding/editing tasks, and connecting to the database.
* It also makes routing and form handling simple with its views and templates.

    Also, since Django uses Python (a popular and easy language), it’s a great choice for students or beginner developers.

### Database

* **Neon** gives PostgreSQL on the cloud for free, so it can easily connect the Django app to it and store data (like todo items, user accounts, etc.) without installing anything on the computer.

    It’s perfect for students or small projects, and it works well with Django using the built-in database tools (ORM).


### Image Storage

* **Cloudinary** is a cloud-based service that makes it easy to upload, store, and manage images.
* It gives a secure image URL after uploading, which can be saved in the database.
* It also helps reduce the load on the main server and speeds up image delivery.

    It is helpful when users want to attach a photo to their task, for example, a screenshot, a document, or a reference image.

## Database

This project uses **PostgreSQL (via Neon)** as the database, and the schema is handled by **Django ORM**.


### Database schema
![database schema](https://github.com/user-attachments/assets/61527395-ddb8-42f8-98da-449183894fa9)


**Tables in the Database:**

1. **User** (from Django’s built-in `auth_user`)
   * Handles user accounts (username, password, email, etc.)
2. **TodoItem**

| Field Name   | Type                    | Description                                        |
|--------------|-------------------------|----------------------------------------------------|
| `id`           | AutoField (Primary)     | Unique ID for each todo item                      |
| `user`         | ForeignKey (User)       | The user who owns this todo item                  |
| `title`        | CharField               | The title of the todo item                        |
| `description`  | TextField (optional)    | Details about the task                            |
| `status`       | CharField (choices)     | Task status: Pending, In Progress, or Completed   |
| `image`        | CloudinaryField         | (Optional) image uploaded to Cloudinary           |
| `created_at`   | DateTimeField           | Automatically set when the task is created        |
| `updated_at`   | DateTimeField           | Automatically updated whenever the task changes   |

### Relationships

1. One User can have many TodoItems.
2. Each TodoItem belongs to one User.

## GitHub Repository

The source code is hosted on GitHub and can be accessed via the following link: [https://github.com/thorungb/TikTasks](https://github.com/thorungb/TikTasks)

### Project Structure

```
TIKTASKS/
├── todo_project/         # Main Django project folder
│   ├── __init__.py
│   ├── asgi.py           # For handling asynchronous server communication
│   ├── settings.py       # Project settings (apps, database config, etc.)
│   ├── urls.py           # URL routes for the whole project
│   ├── wsgi.py           # Web server gateway interface (for deployment)
│   └── __pycache__/      # Auto-generated cache files (Python internal)
│
├── todo_app/             # Main application for managing todo features
│   ├── __init__.py
│   ├── admin.py          # Admin panel configurations
│   ├── apps.py           # App config for Django
│   ├── forms.py          # Django forms (e.g., for task creation, login, etc.)
│   ├── models.py         # Database models (e.g., TodoItem model)
│   ├── tests.py          # Unit tests for this app
│   ├── urls.py           # URL routes specific to this app
│   ├── views.py          # Main logic: handles requests and responses
│   ├── migrations/       # Auto-generated database migration files
│   └── templates/        # HTML frontend templates
│       ├── base.html         # Base layout for other pages
│       ├── login.html        # Login page
│       ├── register.html     # Signup page
│       └── todo_list.html    # Displays a list of todo items
│
├── manage.py            # Django command-line tool (run server, migrate, etc.)
├── .env.sample          # Sample environment variables (e.g., DB credentials, API keys)
├── .gitignore           # Tells Git which files/folders to ignore (e.g., __pycache__, .env)
├── README.md            # Main project description and instructions
├── requirements.txt     # List of Python packages needed for the project
└── installation.md      # Step-by-step setup guide for installing the project
```

## Installation and Running the Application

1. Clone the repository from GitHub.

    ```
    git clone https://github.com/thorungb/TikTasks.git
    ```

2. Create and activate a virtual environment:

    ```
    python -m venv env 
    source env/bin/activate		# macOS/Linux
    env\Scripts\activate		# Windows 
    ```

3. Install required packages using

    ```
    pip install -r requirements.txt
    ```

4. Set up a database and configure database settings in .env

    ```
    cp .env.example .env
    ```

5. Navigate to the todo_project directory

    ```
    cd todo_project
    ```

6. Apply database migrations

    ```
    python manage.py migrate
    ```

7. Start the Django development server

    ```
    python manage.py runserver
    ```

8. Access the application which will be available at

    ```
    http://127.0.0.1:8000/
    ```

## Software Architecture

This project follows the **Layered Architecture**, which helps separate responsibilities clearly between different parts of the system. Each layer has a specific role, making the code more maintainable, testable, and scalable.

1. **Presentation Layer (Front-end)**

	This layer is responsible for the user interface and user interactions. It’s built using HTML, CSS, and JavaScript.

   * Display pages like login, register, and the todo list.
   * Collect user input (e.g., typing a task or clicking a button).
   * Send requests to the backend (via form submission or JavaScript fetch).
   * Dynamically update the UI using JavaScript (e.g., changing task status without refreshing the page).

    This layer is stored in `templates/`

   * `login.html`, `register.html` – User authentication pages.
   * `todo_list.html` – Displays todos and includes JavaScript for status updates or deletions.
   * `base.html` – Shared layout across templates.

2. **Application Layer (Views)**
    
    This layer processes all the logic between the frontend and backend. When a user interacts with the page, this layer decides what to do, fetches/updates data, and returns a response. Centralizing the logic here makes the code easy to manage and lets us keep business rules out of the UI layer.

   * `views.py` – Handles core actions like login, logout, add/edit/delete a todo.
   * `forms.py` – Defines Django forms for validating user input.
   * `urls.py` – Connects each URL to its corresponding view.
  
3. **Domain Layer (Models)**

   This layer defines the structure and logic of data — in other words, what a "Todo Item" or "User" means. This separation ensures all business logic and data structure are in one place, making it easy to reuse and modify.

    This layer is in `models.py`

   * `TodoItem` – model with fields like `title`, `status`, `image`, `user`, etc.
   * Uses relationships to connect todos to users.
  
4. **Infrastructure Layer (Database, Cloud Services)**

    This layer handles external services for data storage and file management.

   * `PostgreSQL (via Neon)` – Stores structured data like user accounts and to-do items.
   * `Cloudinary `– Manages image uploads linked to each todo.
   * `Django ORM` – Automatically converts Python objects into SQL queries to interact with the database.

## Code Explanation

### Backend

The backend of the TikTasks application is built using **Django** with a **Neon PostgreSQL** database and **Cloudinary** for media file storage (like images).

**Main project:** `todo_project/`

* `settings.py`
    * Configures the whole project: installed apps, middleware, templates, database (Neon), Cloudinary setup, etc.
* `urls.py`
    * Main URL router; sends URLs to the right app (e.g., todo_app).
* `wsgi.py & asgi.py`
    * Entry points for running the project with WSGI/ASGI servers (e.g., for deployment).

**App logic:** `todo_app/`

* `admin.py`
    * Registers your models (like Task) for the Django admin panel.
* `apps.py`
    * The configuration file that helps Django recognize the app.
* `forms.py`
    * Defines Django form classes (e.g., for registration, task creation).
* `models.py`
    * Contains data models (like user tasks) that map to Neon database tables.
* `views.py`
    * Core logic for handling requests: e.g., displaying tasks, logging in users, or registering.
* `urls.py`
    * Routes app-specific URLs like /login, /todo, etc.
* `tests.py`
    * Automated tests for the app features.

### Frontend

The frontend uses standard **HTML, CSS, and JavaScript**, rendered via Django’s template system.

**Templates:** `templates/`

* `base.html`
    * The layout that other templates extend (DRY principle).
* `login.html, register.html`
    * Forms for user authentication.
* `todo_list.html`
    * Displays the list of tasks for a logged-in user.
