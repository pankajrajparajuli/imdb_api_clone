# 🎬 IMDB API Clone

An intelligent, authenticated API for managing movies, streaming platforms, and reviews. Built with **Django REST Framework**, it features user authentication, token-based security, and role-based permissions.

---

## 🧠 App Summary

This app provides:

- ✅ User registration, login, and logout  
- 🎥 Movie (WatchList) management (CRUD)  
- 📺 Streaming platform management (CRUD)  
- ⭐ User review system with ratings & text reviews  
- 🔐 Token-based authentication (DRF Token Auth)  
- 👤 Role-based permissions (Admin-only & owner-only actions)  

---

## 🔐 Authentication APIs

| Method | Endpoint              | Description                                  |
|--------|-----------------------|----------------------------------------------|
| POST   | `/api/register/`      | Register a new user                          |
| POST   | `/api/login/`         | Log in user and receive an auth token        |
| POST   | `/api/logout/`        | Logout user and invalidate current token     |

---

## 🎥 WatchList (Movies) APIs

| Method | Endpoint                        | Description                           |
|--------|---------------------------------|---------------------------------------|
| GET    | `/api/watchlist/`              | List all movies                       |
| POST   | `/api/watchlist/`              | Create a new movie *(admin only)*     |
| GET    | `/api/watchlist/{id}/`         | Retrieve details of a movie           |
| PUT    | `/api/watchlist/{id}/`         | Update an existing movie *(admin)*    |
| DELETE | `/api/watchlist/{id}/`         | Delete a movie *(admin only)*         |

---

## 📺 Streaming Platforms APIs

| Method | Endpoint                                 | Description                           |
|--------|------------------------------------------|---------------------------------------|
| GET    | `/api/streaming-platforms/`             | List all streaming platforms          |
| POST   | `/api/streaming-platforms/`             | Create a new platform *(admin only)*  |
| GET    | `/api/streaming-platforms/{id}/`        | Retrieve details of a platform        |
| PUT    | `/api/streaming-platforms/{id}/`        | Update a platform *(admin only)*      |
| DELETE | `/api/streaming-platforms/{id}/`        | Delete a platform *(admin only)*      |

---

## ⭐ Reviews APIs

| Method | Endpoint                                         | Description                                      |
|--------|--------------------------------------------------|--------------------------------------------------|
| GET    | `/api/watchlist/{watchlist_id}/reviews/`        | List reviews for a specific movie                |
| POST   | `/api/watchlist/{watchlist_id}/reviews-create/` | Create a new review *(auth required)*            |
| GET    | `/api/reviews/{id}/`                            | Retrieve details of a review                      |
| PUT    | `/api/reviews/{id}/`                            | Update a review *(owner only)*                   |
| DELETE | `/api/reviews/{id}/`                            | Delete a review *(owner only)*                   |

---

## 🧑‍💼 Admin APIs (Django Admin Panel)

| Access | URL                      | Description                  |
|--------|--------------------------|------------------------------|
| GET    | `/admin/`                | Admin login dashboard        |
| GET    | `/admin/watchlist_app/`  | Manage movies, platforms, reviews, users |

> ℹ️ All admin endpoints are accessible via the Django admin panel.  
> Requires login with superuser credentials.

---

## 📦 Tech Stack

- Python 3.10+  
- Django 5.x  
- Django REST Framework  
- PostgreSQL
- DRF Token Authentication
- JWT Token Authentication

---

## 🚀 How to Use

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/imdb-api-clone.git
   cd imdb-api-clone
2. **Create virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
3. **Apply migrations & run the server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   
4. ***Access the API***
    Visit http://127.0.0.1:8000/api/
