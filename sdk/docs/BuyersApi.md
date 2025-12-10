# BuyersApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**addToCartApiV1BuyersCartPost**](#addtocartapiv1buyerscartpost) | **POST** /api/v1/buyers/cart | Add To Cart|
|[**checkoutApiV1BuyersCheckoutPost**](#checkoutapiv1buyerscheckoutpost) | **POST** /api/v1/buyers/checkout | Checkout|
|[**clearCartApiV1BuyersCartDelete**](#clearcartapiv1buyerscartdelete) | **DELETE** /api/v1/buyers/cart | Clear Cart|
|[**getCartApiV1BuyersCartGet**](#getcartapiv1buyerscartget) | **GET** /api/v1/buyers/cart | Get Cart|
|[**getOrderApiV1BuyersOrdersOrderIdGet**](#getorderapiv1buyersordersorderidget) | **GET** /api/v1/buyers/orders/{order_id} | Get Order|
|[**getOrdersApiV1BuyersOrdersGet**](#getordersapiv1buyersordersget) | **GET** /api/v1/buyers/orders | Get Orders|
|[**getProductApiV1BuyersProductsProductIdGet**](#getproductapiv1buyersproductsproductidget) | **GET** /api/v1/buyers/products/{product_id} | Get Product|
|[**getProductsApiV1BuyersProductsGet**](#getproductsapiv1buyersproductsget) | **GET** /api/v1/buyers/products | Get Products|
|[**removeFromCartApiV1BuyersCartItemIdDelete**](#removefromcartapiv1buyerscartitemiddelete) | **DELETE** /api/v1/buyers/cart/{item_id} | Remove From Cart|
|[**updateCartItemApiV1BuyersCartItemIdPut**](#updatecartitemapiv1buyerscartitemidput) | **PUT** /api/v1/buyers/cart/{item_id} | Update Cart Item|

# **addToCartApiV1BuyersCartPost**
> any addToCartApiV1BuyersCartPost(cartItemCreate)

Add item to cart

### Example

```typescript
import {
    BuyersApi,
    Configuration,
    CartItemCreate
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let cartItemCreate: CartItemCreate; //

const { status, data } = await apiInstance.addToCartApiV1BuyersCartPost(
    cartItemCreate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **cartItemCreate** | **CartItemCreate**|  | |


### Return type

**any**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **checkoutApiV1BuyersCheckoutPost**
> CheckoutResponse checkoutApiV1BuyersCheckoutPost(body)

Process checkout and create order

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let body: object; //

const { status, data } = await apiInstance.checkoutApiV1BuyersCheckoutPost(
    body
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **body** | **object**|  | |


### Return type

**CheckoutResponse**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clearCartApiV1BuyersCartDelete**
> any clearCartApiV1BuyersCartDelete()

Clear all items from cart

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

const { status, data } = await apiInstance.clearCartApiV1BuyersCartDelete();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**any**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getCartApiV1BuyersCartGet**
> Array<CartItemWithProductResponse> getCartApiV1BuyersCartGet()

Get user\'s cart items

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

const { status, data } = await apiInstance.getCartApiV1BuyersCartGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<CartItemWithProductResponse>**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getOrderApiV1BuyersOrdersOrderIdGet**
> OrderResponse getOrderApiV1BuyersOrdersOrderIdGet()

Get specific order details

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let orderId: string; // (default to undefined)

const { status, data } = await apiInstance.getOrderApiV1BuyersOrdersOrderIdGet(
    orderId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderId** | [**string**] |  | defaults to undefined|


### Return type

**OrderResponse**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getOrdersApiV1BuyersOrdersGet**
> Array<OrderResponse> getOrdersApiV1BuyersOrdersGet()

Get user\'s order history

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

const { status, data } = await apiInstance.getOrdersApiV1BuyersOrdersGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<OrderResponse>**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProductApiV1BuyersProductsProductIdGet**
> ProductResponse getProductApiV1BuyersProductsProductIdGet()

Get a single product by ID

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let productId: string; // (default to undefined)

const { status, data } = await apiInstance.getProductApiV1BuyersProductsProductIdGet(
    productId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **productId** | [**string**] |  | defaults to undefined|


### Return type

**ProductResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProductsApiV1BuyersProductsGet**
> ProductListResponse getProductsApiV1BuyersProductsGet()

Get paginated list of products with filtering

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let page: number; // (optional) (default to 1)
let perPage: number; // (optional) (default to 20)
let priceMin: number; // (optional) (default to undefined)
let priceMax: number; // (optional) (default to undefined)
let productType: string; // (optional) (default to undefined)
let search: string; // (optional) (default to undefined)
let sort: string; // (optional) (default to 'created_at')
let order: string; // (optional) (default to 'desc')

const { status, data } = await apiInstance.getProductsApiV1BuyersProductsGet(
    page,
    perPage,
    priceMin,
    priceMax,
    productType,
    search,
    sort,
    order
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] |  | (optional) defaults to 1|
| **perPage** | [**number**] |  | (optional) defaults to 20|
| **priceMin** | [**number**] |  | (optional) defaults to undefined|
| **priceMax** | [**number**] |  | (optional) defaults to undefined|
| **productType** | [**string**] |  | (optional) defaults to undefined|
| **search** | [**string**] |  | (optional) defaults to undefined|
| **sort** | [**string**] |  | (optional) defaults to 'created_at'|
| **order** | [**string**] |  | (optional) defaults to 'desc'|


### Return type

**ProductListResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **removeFromCartApiV1BuyersCartItemIdDelete**
> any removeFromCartApiV1BuyersCartItemIdDelete()

Remove item from cart

### Example

```typescript
import {
    BuyersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let itemId: string; // (default to undefined)

const { status, data } = await apiInstance.removeFromCartApiV1BuyersCartItemIdDelete(
    itemId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **itemId** | [**string**] |  | defaults to undefined|


### Return type

**any**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateCartItemApiV1BuyersCartItemIdPut**
> CartItemResponse updateCartItemApiV1BuyersCartItemIdPut(cartItemUpdate)

Update cart item quantity

### Example

```typescript
import {
    BuyersApi,
    Configuration,
    CartItemUpdate
} from './api';

const configuration = new Configuration();
const apiInstance = new BuyersApi(configuration);

let itemId: string; // (default to undefined)
let cartItemUpdate: CartItemUpdate; //

const { status, data } = await apiInstance.updateCartItemApiV1BuyersCartItemIdPut(
    itemId,
    cartItemUpdate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **cartItemUpdate** | **CartItemUpdate**|  | |
| **itemId** | [**string**] |  | defaults to undefined|


### Return type

**CartItemResponse**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

