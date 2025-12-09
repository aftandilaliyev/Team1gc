# Gem Store Backend Setup Guide

## Prerequisites
- Python 3.12+
- MySQL database
- DodoPayments account (for payment processing)
- DodoPayments SDK (automatically installed)

## Installation

1. **Clone and navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   # Database
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=team1gc_db
   
   # JWT
   SECRET_KEY=your-very-secure-secret-key
   
   # DodoPayments
   DODO_PAYMENTS_API_KEY=your-dodo-payments-api-key
   DODO_PAYMENTS_WEBHOOK_SECRET=your-webhook-secret
   
   # URLs
   FRONTEND_URL=http://localhost:3000
   BACKEND_URL=http://localhost:8000
   ```

4. **Set up the database**
   ```bash
   # Create database
   mysql -u root -p -e "CREATE DATABASE team1gc_db;"
   
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

5. **Run the application**
   ```bash
   # Development mode
   python src/main.py
   
   # Or using uvicorn directly
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

The API will be available at `http://localhost:8000`

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## User Roles and Functionality

### Buyers (Role: 0)
- Browse and search products
- Add items to cart
- Checkout with DodoPayments integration
- View order history

### Sellers (Role: 1)
- Create and manage products
- View orders containing their products
- Approve and ship orders
- View sales analytics

### Suppliers (Role: 2)
- View all orders in the system
- Approve confirmed orders
- Update order status (ship, deliver, cancel)
- View system-wide analytics

## Testing the API

1. **Register a user**
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "buyer@example.com",
       "username": "buyer1",
       "password": "password123",
       "role": "buyer"
     }'
   ```

2. **Login to get JWT token**
   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "buyer1",
       "password": "password123"
     }'
   ```

3. **Use the token for authenticated requests**
   ```bash
   curl -X GET "http://localhost:8000/api/buyers/cart" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## DodoPayments Integration

To test payment functionality:

1. Set up a DodoPayments account
2. Get your API key and webhook secret
3. Configure webhook URL: `http://your-domain.com/api/webhooks/dodo-payments`
4. Test checkout flow through the buyer endpoints

## Development Notes

- The application uses FastAPI with SQLAlchemy ORM
- JWT tokens are used for authentication
- Role-based access control is implemented
- Payment processing is handled via DodoPayments webhooks
- All endpoints return JSON responses
- Comprehensive error handling with proper HTTP status codes

## Troubleshooting

**Database Connection Issues:**
- Ensure MySQL is running
- Check database credentials in `.env`
- Verify database exists

**Import Errors:**
- Run `uv sync` to install all dependencies
- Ensure Python 3.12+ is being used

**Authentication Issues:**
- Check JWT secret key configuration
- Verify token format in Authorization header
- Ensure user account is active

**Payment Issues:**
- Verify DodoPayments API credentials
- Check webhook URL configuration
- Review webhook signature validation
