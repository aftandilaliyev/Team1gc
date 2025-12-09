# Gem Store API Documentation

## Overview
This API provides functionality for a gem store with three user roles: Buyers, Sellers, and Suppliers.

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## User Roles

### Buyer (Role: 0)
- View products (stones)
- Add items to cart
- Checkout and create orders
- View order history

### Seller (Role: 1) 
- Create, read, update, delete products
- View orders containing their products
- Approve orders (move from pending to confirmed)
- Ship orders (move from confirmed to shipped)

### Supplier (Role: 2)
- View all orders
- Approve orders (move from confirmed to shipped)
- Update order status (ship, deliver, cancel)
- View system-wide analytics

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Public Product Endpoints
- `GET /api/products/` - Get paginated products with filtering
- `GET /api/products/{product_id}` - Get single product

### Buyer Endpoints
- `GET /api/buyers/products` - Get products with buyer-specific filtering
- `POST /api/buyers/cart` - Add item to cart
- `GET /api/buyers/cart` - Get cart items
- `PUT /api/buyers/cart/{item_id}` - Update cart item quantity
- `DELETE /api/buyers/cart/{item_id}` - Remove item from cart
- `DELETE /api/buyers/cart` - Clear entire cart
- `POST /api/buyers/checkout` - Process checkout and create order
- `GET /api/buyers/orders` - Get order history
- `GET /api/buyers/orders/{order_id}` - Get specific order

### Seller Endpoints
- `POST /api/sellers/products` - Create new product
- `GET /api/sellers/products` - Get seller's products
- `GET /api/sellers/products/{product_id}` - Get specific product
- `PUT /api/sellers/products/{product_id}` - Update product
- `DELETE /api/sellers/products/{product_id}` - Delete product
- `GET /api/sellers/orders` - Get orders containing seller's products
- `GET /api/sellers/orders/{order_id}` - Get specific order
- `PUT /api/sellers/orders/{order_id}` - Update order status (approve/ship)
- `GET /api/sellers/analytics` - Get seller analytics

### Supplier Endpoints
- `GET /api/suppliers/orders/pending` - Get orders needing approval
- `GET /api/suppliers/orders` - Get all orders
- `GET /api/suppliers/orders/{order_id}` - Get specific order
- `POST /api/suppliers/orders/{order_id}/approve` - Approve order
- `PUT /api/suppliers/orders/{order_id}` - Update order status
- `GET /api/suppliers/analytics` - Get supplier analytics

### Webhook Endpoints
- `POST /api/webhooks/dodo-payments` - DodoPayments webhook handler

## Order Status Flow

1. **PENDING** - Order created, payment pending
2. **CONFIRMED** - Payment successful (via DodoPayments webhook)
3. **SHIPPED** - Order approved and shipped by seller/supplier
4. **DELIVERED** - Order delivered to customer
5. **CANCELLED** - Order cancelled (payment failed or manual cancellation)

## Status Transition Rules

### Sellers can:
- PENDING → CONFIRMED (approve order)
- CONFIRMED → SHIPPED (ship order)

### Suppliers can:
- CONFIRMED → SHIPPED (approve and ship)
- SHIPPED → DELIVERED (mark as delivered)
- Any status → CANCELLED (cancel order)

## DodoPayments Integration

The system integrates with DodoPayments using the official SDK for payment processing:

1. **Checkout Process**:
   - User initiates checkout
   - System creates order and payment intent with DodoPayments
   - User redirected to DodoPayments checkout page
   - Payment success/failure handled via webhooks

2. **Webhook Events**:
   - `payment.succeeded` - Confirms order
   - `payment.failed` - Cancels order
   - `payment.refunded` - Cancels order

## Environment Variables

Required environment variables for DodoPayments:
```
DODO_PAYMENTS_API_KEY=your-api-key
DODO_PAYMENTS_BASE_URL=https://api.dodopayments.com
DODO_PAYMENTS_WEBHOOK_SECRET=your-webhook-secret
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

## Error Handling

The API returns standard HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Data Models

### Product
- `id` (UUID) - Unique identifier
- `seller_id` (UUID) - Seller who owns the product
- `type_id` (UUID) - Product category/type
- `name` (string) - Product name
- `price` (decimal) - Product price
- `description` (string) - Product description
- `images` (array) - Product images
- `created_at` / `updated_at` (datetime)

### Order
- `id` (UUID) - Unique identifier
- `user_id` (int) - Buyer who placed the order
- `status` (enum) - Order status
- `total_amount` (decimal) - Total order amount
- `shipping_address` (string) - Delivery address
- `billing_address` (string) - Billing address
- `items` (array) - Order items with quantities and prices
- `created_at` / `updated_at` (datetime)

### Cart Item
- `id` (UUID) - Unique identifier
- `user_id` (int) - User who owns the cart item
- `product_id` (UUID) - Product in cart
- `quantity` (int) - Quantity of product
