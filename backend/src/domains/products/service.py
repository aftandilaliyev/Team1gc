from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from fastapi import HTTPException, status

from src.shared.models.product import Product, ProductImage
from src.shared.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse, ProductQueryParams
)


class ProductService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def query_products(
        self,
        page: int = 1,
        elements: int = 20,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        category: Optional[UUID] = None,
        sort: str = "created_at",
        search: Optional[str] = None
    ) -> ProductListResponse:
        """Query products with filtering, sorting, and pagination"""
        query = self.session.query(Product)
        
        # Apply filters
        if price_min is not None:
            query = query.filter(Product.price >= price_min)
        
        if price_max is not None:
            query = query.filter(Product.price <= price_max)
        
        if category:
            query = query.filter(Product.type_id == category)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Apply sorting
        sort_column = getattr(Product, sort, Product.created_at)
        query = query.order_by(desc(sort_column))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * elements
        products = query.offset(offset).limit(elements).all()
        
        # Calculate total pages
        total_pages = (total + elements - 1) // elements
        
        return ProductListResponse(
            products=[ProductResponse.model_validate(product) for product in products],
            total=total,
            page=page,
            per_page=elements,
            total_pages=total_pages
        )

    def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        """Get a single product by ID"""
        product = self.session.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return ProductResponse.model_validate(product)

    def create_product(self, seller_id: int, create_product_schema: ProductCreate) -> ProductResponse:
        """Create a new product"""
        # Create product
        product = Product(
            seller_id=seller_id,
            name=create_product_schema.name,
            price=create_product_schema.price,
            description=create_product_schema.description,
            type_id=create_product_schema.type_id
        )
        
        self.session.add(product)
        self.session.flush()  # Get product ID
        
        # Add images if provided
        for image_data in create_product_schema.images:
            image = ProductImage(
                product_id=product.id,
                image_url=image_data.image_url
            )
            self.session.add(image)
        
        self.session.commit()
        self.session.refresh(product)
        
        return ProductResponse.model_validate(product)

    def update_product(self, product_id: UUID, seller_id: int, update_product_schema: ProductUpdate) -> ProductResponse:
        """Update an existing product"""
        product = self.session.query(Product).filter(
            and_(
                Product.id == product_id,
                Product.seller_id == seller_id
            )
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or access denied"
            )
        
        # Update fields if provided
        if update_product_schema.name is not None:
            product.name = update_product_schema.name
        
        if update_product_schema.price is not None:
            product.price = update_product_schema.price
        
        if update_product_schema.description is not None:
            product.description = update_product_schema.description
        
        if update_product_schema.type_id is not None:
            product.type_id = update_product_schema.type_id
        
        self.session.commit()
        self.session.refresh(product)
        
        return ProductResponse.model_validate(product)

    def delete_product(self, product_id: UUID, seller_id: int) -> None:
        """Delete a product"""
        product = self.session.query(Product).filter(
            and_(
                Product.id == product_id,
                Product.seller_id == seller_id
            )
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or access denied"
            )
        
        self.session.delete(product)
        self.session.commit()

    def get_products_by_seller(self, seller_id: int, page: int = 1, per_page: int = 20) -> ProductListResponse:
        """Get all products for a specific seller"""
        query = self.session.query(Product).filter(Product.seller_id == seller_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        products = query.order_by(desc(Product.created_at)).offset(offset).limit(per_page).all()
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        return ProductListResponse(
            products=[ProductResponse.model_validate(product) for product in products],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
