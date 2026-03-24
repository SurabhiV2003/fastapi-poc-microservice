POC 1 – 1 Day
FastAPI Microservice with Auditing & Logging based on your requirements:
Overview
Goal:
• Build a FastAPI microservice that:
o Uses SQLite as the database.
o Has 5 tables with relationships (joins).
o Supports filtering, data transformation (massage), and retrieval.
o Implements auditing of requests/responses, structured logging, and global exception handling.
o Exposes REST endpoints and includes a consumer script to call the service.
Database Schema - Postgre
We’ll create 5 tables with realistic relationships:
1. users
o id (PK), name, email, role
2. products
o id (PK), name, price, category
3. orders
o id (PK), user_id (FK → users.id), order_date
4. order_items
o id (PK), order_id (FK → orders.id), product_id (FK → products.id), quantity
5. audit_logs
o id (PK), timestamp, endpoint, request_payload, response_payload, status_code
Relationships:
• users ↔ orders (One-to-Many)
• orders ↔ order_items (One-to-Many)
• order_items ↔ products (Many-to-One)
Core Features
• CRUD Endpoints:
o /users, /products, /orders
• Complex Query:
o Get all orders for a user with product details (JOIN across tables).
o Filter by date range, product category, or price.
• Data Massage:
o Transform response to include totals, summaries.
• Auditing:
o Middleware to log request/response in audit_logs.
• Logging:
o Use logging module with structured JSON logs.
• Global Exception Handling:
o Custom error handler for validation and server errors.
Service Exposure
• FastAPI app with endpoints.
• Swagger UI for testing.
• Consumer Script:
o Python script using requests to call APIs and print results.
Deployment
• Dockerfile for containerization.
• Run locally or deploy to Kubernetes/Azure App Service.
Next Steps
You can now:
1. Generate full FastAPI project code:
o DB models (SQLAlchemy + SQLite).
o CRUD routes.
o Middleware for auditing.
o Logging setup.
o Exception handling.
o Consumer script.
2. Provide architecture diagram and README for setup.
fastapi-poc-microservice/
├── app/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── database.py      # SQLite connection logic
│   ├── models.py        # SQLAlchemy tables (User, Product, etc.)
│   ├── schemas.py       # Pydantic models (Data validation)
│   ├── crud.py          # Create, Read, Update, Delete logic
│   └── middleware.py    # Auditing & Logging logic
├── consumer.py          # Script to test your API
├── requirements.txt     # List of libraries
└── .gitignore           # Files to exclude from GitHub
 

 Models has tables: 
 * Users
 * Product
 * Order
 * OrderItem
 * AuditLog
 