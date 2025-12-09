# Frontend Pages Documentation

This document describes the frontend pages created for the e-commerce platform.

## Pages Overview

### 1. Home Page (`/`)
- **File**: `app/page.js`
- **Description**: Landing page with platform overview and call-to-action buttons
- **Features**:
  - Hero section with platform introduction
  - Feature highlights (Shop, Sell, Security)
  - Navigation to catalog and registration

### 2. Authentication Pages

#### Login Page (`/login`)
- **File**: `app/login/page.jsx`
- **Description**: User login form
- **Features**:
  - Username/password authentication
  - Error handling
  - Redirect to dashboard after successful login
  - Link to registration page

#### Register Page (`/register`)
- **File**: `app/register/page.jsx`
- **Description**: User registration form
- **Features**:
  - User registration with role selection (buyer/seller/supplier)
  - Form validation
  - Password confirmation
  - Redirect to login after successful registration

### 3. Product Catalog (`/catalog`)
- **File**: `app/catalog/page.jsx`
- **Description**: Product browsing and search
- **Features**:
  - Product grid display with images, prices, and descriptions
  - Search and filtering (price range, sorting)
  - Pagination
  - Add to cart functionality
  - Stock status display

### 4. Buyer Pages

#### Shopping Cart (`/cart`)
- **File**: `app/cart/page.jsx`
- **Description**: Shopping cart management
- **Features**:
  - View cart items with product details
  - Update item quantities
  - Remove items from cart
  - Clear entire cart
  - Order summary with total calculation
  - Checkout process

#### Orders History (`/orders`)
- **File**: `app/orders/page.jsx`
- **Description**: Order history and tracking
- **Features**:
  - List of all user orders
  - Order status tracking
  - Order details modal
  - Shipping information display
  - Order item breakdown

### 5. Seller Dashboard (`/seller/dashboard`)
- **File**: `app/seller/dashboard/page.jsx`
- **Description**: Seller management interface
- **Features**:
  - Analytics overview (products, orders, revenue)
  - Product management (CRUD operations)
  - Order management with status updates
  - Product form modal for adding/editing
  - Tabbed interface for products and orders

### 6. Dashboard Redirect (`/dashboard`)
- **File**: `app/dashboard/page.jsx`
- **Description**: Role-based dashboard redirect
- **Features**:
  - Redirects users to appropriate dashboard based on role
  - Handles authentication check

## Components

### Navigation Component
- **File**: `components/Navigation.jsx`
- **Description**: Main navigation bar
- **Features**:
  - Role-based navigation links
  - User authentication status
  - Logout functionality
  - Responsive design

### Authentication Context
- **File**: `contexts/AuthContext.jsx`
- **Description**: Authentication state management
- **Features**:
  - Global authentication state
  - Token management with SDK integration
  - Login/logout functions
  - User data persistence

## API Integration

All pages use the existing SDK (`sdk/sdk.ts`) for API communication:

- **Authentication API**: Login, register, get current user
- **Products API**: Get products with filtering and pagination
- **Buyers API**: Cart management, checkout, order history
- **Sellers API**: Product CRUD, order management, analytics

## Key Features

1. **Responsive Design**: All pages are mobile-friendly using TailwindCSS
2. **Error Handling**: Comprehensive error messages and loading states
3. **Authentication**: Protected routes with role-based access
4. **Real-time Updates**: Cart and order status updates
5. **Form Validation**: Client-side validation for all forms
6. **User Experience**: Loading states, confirmation dialogs, and success messages

## Usage Instructions

1. **Setup**: Ensure the backend API is running and the SDK is properly configured
2. **Environment**: Set `NEXT_PUBLIC_API_URL` environment variable for API base URL
3. **Development**: Run `npm run dev` to start the development server
4. **Authentication**: Users must register and login to access protected features
5. **Roles**: Different user roles (buyer/seller) have access to different features

## Future Enhancements

- Supplier dashboard and functionality
- Product categories and advanced filtering
- Image upload for products
- Payment integration
- Real-time notifications
- Advanced analytics and reporting
- Product reviews and ratings
