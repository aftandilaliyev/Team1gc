# Gem Store E-Commerce Platform

A full-stack e-commerce platform for buying and selling gemstones, built with FastAPI and Next.js. The platform supports three distinct user roles: Buyers, Sellers, and Suppliers, each with role-specific functionality.

## 🚀 Features

### For Buyers
- Browse and search product catalog
- Add items to shopping cart
- Secure checkout with payment processing
- View order history and track order status
- Real-time stock availability

### For Sellers
- Create, update, and manage products
- Upload product images
- View orders containing their products
- Approve and ship orders
- Sales analytics and insights

### For Suppliers
- View all system orders
- Manage order fulfillment
- Update order status (ship, deliver, cancel)
- System-wide analytics

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Payment Processing**: DodoPayments integration
- **File Storage**: AWS S3 (via boto3)
- **API Documentation**: Swagger UI and ReDoc

### Frontend
- **Framework**: Next.js 16 with React 19
- **Styling**: TailwindCSS 4
- **State Management**: React Context API
- **API Client**: Auto-generated TypeScript SDK

## 📁 Project Structure

```
Team1gc/
├── backend/                 # FastAPI backend application
│   ├── src/
│   │   ├── core/           # API setup and logging
│   │   ├── domains/         # Business logic by domain
│   │   │   ├── auth/       # Authentication
│   │   │   ├── buyers/     # Buyer endpoints
│   │   │   ├── sellers/    # Seller endpoints
│   │   │   ├── suppliers/  # Supplier endpoints
│   │   │   ├── products/   # Product management
│   │   │   ├── webhooks/   # Payment webhooks
│   │   │   └── uploads/    # File uploads
│   │   ├── infrastructure/ # External services
│   │   │   ├── database/   # Database connection
│   │   │   ├── bucket/     # S3 storage
│   │   │   ├── payments/   # Payment processing
│   │   │   └── emails/     # Email service
│   │   ├── shared/         # Shared utilities
│   │   │   ├── models/     # SQLAlchemy models
│   │   │   ├── schemas/    # Pydantic schemas
│   │   │   ├── config/     # Configuration
│   │   │   └── utils/      # Helper functions
│   │   └── main.py         # Application entry point
│   ├── tests/              # Test suite
│   ├── docker-compose.yml  # Docker services (backend only)
│   └── pyproject.toml      # Python dependencies
│
├── frontend/               # Next.js frontend application
│   ├── app/                # Next.js app directory
│   │   ├── catalog/        # Product catalog page
│   │   ├── cart/           # Shopping cart page
│   │   ├── orders/         # Order history page
│   │   ├── login/          # Login page
│   │   ├── register/       # Registration page
│   │   ├── seller/         # Seller dashboard
│   │   └── supplier/       # Supplier dashboard
│   ├── components/         # React components
│   ├── contexts/           # React contexts
│   └── lib/                # Utilities and API client
│
├── sdk/                    # Auto-generated TypeScript SDK
├── images/                 # Product images
└── docs/                   # Additional documentation
```

## 🛠️ Prerequisites

- **Docker** and **Docker Compose** (for backend containerized setup)
- **Node.js** 18+ and **npm** (for frontend development - required)
- **Python** 3.12+ and **uv** (for backend development if running manually)
- **MySQL** database (or use Docker Compose for backend)
- **DodoPayments** account (for payment processing)
- **AWS S3** bucket (for file storage)

## 🚀 Quick Start

### Backend Setup (Using Docker Compose)

The backend uses Docker Compose to run the application and MySQL database together.

1. **Clone the repository**
   ```bash
   git clone https://github.com/aftandilaliyev/Team1gc.git
   cd Team1gc
   ```

2. **Set up backend environment variables**
   ```bash
   cd backend
   cp .env.template .env
   # Edit .env with your configuration
   ```

3. **Start the backend services**
   ```bash
   # From backend directory
   docker compose up --build
   ```

   This will start:
   - MySQL database container
   - FastAPI backend application container

   Or use the Makefile:
   ```bash
   make backend-setup  # Setup and start backend with Docker
   ```

### Backend Manual Setup (Alternative)

If you prefer to run the backend manually without Docker:

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   ```bash
   cp .env.template .env
   # Edit .env with your database, JWT, and payment credentials
   ```

4. **Set up database**
   ```bash
   # Create MySQL database (or use Docker Compose for database only)
   mysql -u root -p -e "CREATE DATABASE team1gc_db;"
   
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

5. **Run the backend**
   ```bash
   python src/main.py
   # Or
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup (Manual - Required)

**Note**: The frontend must be run manually. There is no Docker setup for the frontend.

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env.local
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. **Run the frontend**
   ```bash
   npm run dev
   ```

   The frontend will be available at http://localhost:3000

## 🌐 Access Points

Once both services are running:

- **Frontend**: http://localhost:3000 (run manually with `npm run dev`)
- **Backend API**: http://localhost:8000 (via Docker Compose or manual setup)
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

**Important**: Make sure both the backend (port 8000) and frontend (port 3000) are running simultaneously.

## 📚 Documentation

- [Backend API Documentation](./backend/API_DOCUMENTATION.md) - Complete API reference
- [Backend Setup Guide](./backend/SETUP_GUIDE.md) - Detailed backend setup instructions
- [Database Design](./backend/DATABASE_DESIGN.md) - Database schema documentation
- [Frontend Pages Documentation](./frontend/PAGES_README.md) - Frontend pages overview

## 🔐 Environment Variables

### Backend (.env)

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=team1gc_db

# JWT Configuration
SECRET_KEY=your-very-secure-secret-key

# DodoPayments
DODO_PAYMENTS_API_KEY=your-dodo-payments-api-key
DODO_PAYMENTS_WEBHOOK_SECRET=your-webhook-secret

# AWS S3 (for file uploads)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

# Debug Mode
DEBUG=true
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📦 Available Scripts

### Makefile Commands

```bash
make backend-setup  # Setup and start backend with Docker Compose
make backend-down    # Stop backend Docker containers
make frontend-setup  # Install frontend dependencies
make frontend-dev    # Start frontend development server (manual)
make sdk-generate    # Generate TypeScript SDK from OpenAPI spec
make sdk-push        # Push SDK to npm registry
```

**Note**: The frontend must be started manually using `make frontend-dev` or `npm run dev` in the frontend directory.

### Backend Commands

```bash
cd backend
uv sync                    # Install dependencies
python src/main.py         # Run development server
pytest                     # Run tests
alembic upgrade head       # Run database migrations
```

### Frontend Commands

```bash
cd frontend
npm install                # Install dependencies
npm run dev                # Start development server
npm run build              # Build for production
npm run start              # Start production server
npm run lint               # Run ESLint
```

## 🗄️ Database Schema

The application uses MySQL with the following main tables:

- **users** - User accounts and authentication
- **products** - Product catalog
- **product_images** - Product images
- **cart_items** - Shopping cart items
- **orders** - Customer orders
- **order_items** - Items within orders
- **customers** - Payment customer information

See [Database Design](./backend/DATABASE_DESIGN.md) for complete schema documentation.

## 🔄 API SDK

The project includes an auto-generated TypeScript SDK for frontend integration. The SDK is generated from the OpenAPI specification and can be regenerated using:

```bash
make sdk-generate
```

## 🛡️ Security Features

- JWT-based authentication
- Bcrypt password hashing (12 rounds)
- Role-based access control (RBAC)
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Input validation (Pydantic schemas)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of an academic course (Introduction to Software Engineering, Fall 2025).

## 👥 Team

Team 1 - Gem Store (Team1gc)

## 🐛 Troubleshooting

### Backend Issues

- **Database connection errors**: Verify MySQL is running and credentials in `.env` are correct
- **Import errors**: Ensure you've run `uv sync` to install dependencies
- **Port already in use**: Change the port in `src/main.py` or stop the conflicting service

### Frontend Issues

- **API connection errors**: Verify `NEXT_PUBLIC_API_URL` is set correctly and backend is running
- **Build errors**: Clear `.next` directory and `node_modules`, then reinstall dependencies
- **SDK errors**: Regenerate the SDK using `make sdk-generate`

### Docker Issues (Backend Only)

- **Container won't start**: Check Docker logs with `docker compose logs` (from backend directory)
- **Database not accessible**: Ensure MySQL container is running and healthy
- **Port conflicts**: Modify ports in `backend/docker-compose.yml`
- **Backend not accessible**: Ensure you're running Docker Compose from the `backend/` directory

### Frontend Issues

- **Frontend won't start**: Ensure Node.js 18+ is installed and dependencies are installed with `npm install`
- **API connection errors**: Verify `NEXT_PUBLIC_API_URL` is set correctly in `.env.local` and backend is running on port 8000
- **Build errors**: Clear `.next` directory and `node_modules`, then reinstall dependencies
- **SDK errors**: Regenerate the SDK using `make sdk-generate`

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Built with ❤️ by Team 1**

