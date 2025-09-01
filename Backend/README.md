# THS Website Backend

This backend is built with Python Flask and MongoDB. It provides REST API endpoints for:
- User authentication (login/logout)
- Catalog management (view/select products)
- Quotation creation (write/produce quotations)

## Setup Instructions
1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install flask flask-pymongo flask-cors flask-bcrypt flask-jwt-extended
   ```
3. Set up MongoDB (local or Atlas)
4. Run the app:
   ```bash
   python app.py
   ```

## API Endpoints
- `/api/login` - User login
- `/api/catalog` - Get catalog items
- `/api/quotation` - Create/view quotations

## Folder Structure
- `app.py` - Main Flask app
- `models.py` - Data models
- `routes/` - API route handlers
- `config.py` - Configuration

---
Replace placeholder values and endpoints as needed for your deployment.
