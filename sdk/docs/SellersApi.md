# SellersApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**createProductApiV1SellersProductsPost**](#createproductapiv1sellersproductspost) | **POST** /api/v1/sellers/products | Create Product|
|[**deleteProductApiV1SellersProductsProductIdDelete**](#deleteproductapiv1sellersproductsproductiddelete) | **DELETE** /api/v1/sellers/products/{product_id} | Delete Product|
|[**getOrderApiV1SellersOrdersOrderIdGet**](#getorderapiv1sellersordersorderidget) | **GET** /api/v1/sellers/orders/{order_id} | Get Order|
|[**getProductApiV1SellersProductsProductIdGet**](#getproductapiv1sellersproductsproductidget) | **GET** /api/v1/sellers/products/{product_id} | Get Product|
|[**getSellerAnalyticsApiV1SellersAnalyticsGet**](#getselleranalyticsapiv1sellersanalyticsget) | **GET** /api/v1/sellers/analytics | Get Seller Analytics|
|[**getSellerOrdersApiV1SellersOrdersGet**](#getsellerordersapiv1sellersordersget) | **GET** /api/v1/sellers/orders | Get Seller Orders|
|[**getSellerProductsApiV1SellersProductsGet**](#getsellerproductsapiv1sellersproductsget) | **GET** /api/v1/sellers/products | Get Seller Products|
|[**updateOrderStatusApiV1SellersOrdersOrderIdPut**](#updateorderstatusapiv1sellersordersorderidput) | **PUT** /api/v1/sellers/orders/{order_id} | Update Order Status|
|[**updateProductApiV1SellersProductsProductIdPut**](#updateproductapiv1sellersproductsproductidput) | **PUT** /api/v1/sellers/products/{product_id} | Update Product|

# **createProductApiV1SellersProductsPost**
> ProductResponse createProductApiV1SellersProductsPost(productCreate)

Create a new product

### Example

```typescript
import {
    SellersApi,
    Configuration,
    ProductCreate
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let productCreate: ProductCreate; //

const { status, data } = await apiInstance.createProductApiV1SellersProductsPost(
    productCreate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **productCreate** | **ProductCreate**|  | |


### Return type

**ProductResponse**

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

# **deleteProductApiV1SellersProductsProductIdDelete**
> any deleteProductApiV1SellersProductsProductIdDelete()

Delete a product

### Example

```typescript
import {
    SellersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let productId: string; // (default to undefined)

const { status, data } = await apiInstance.deleteProductApiV1SellersProductsProductIdDelete(
    productId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **productId** | [**string**] |  | defaults to undefined|


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

# **getOrderApiV1SellersOrdersOrderIdGet**
> OrderResponse getOrderApiV1SellersOrdersOrderIdGet()

Get specific order details

### Example

```typescript
import {
    SellersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let orderId: string; // (default to undefined)

const { status, data } = await apiInstance.getOrderApiV1SellersOrdersOrderIdGet(
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

# **getProductApiV1SellersProductsProductIdGet**
> ProductResponse getProductApiV1SellersProductsProductIdGet()

Get a specific product by ID

### Example

```typescript
import {
    SellersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let productId: string; // (default to undefined)

const { status, data } = await apiInstance.getProductApiV1SellersProductsProductIdGet(
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

# **getSellerAnalyticsApiV1SellersAnalyticsGet**
> any getSellerAnalyticsApiV1SellersAnalyticsGet()

Get seller analytics dashboard data

### Example

```typescript
import {
    SellersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

const { status, data } = await apiInstance.getSellerAnalyticsApiV1SellersAnalyticsGet();
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

# **getSellerOrdersApiV1SellersOrdersGet**
> Array<OrderResponse> getSellerOrdersApiV1SellersOrdersGet()

Get orders containing seller\'s products

### Example

```typescript
import {
    SellersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let page: number; // (optional) (default to 1)
let perPage: number; // (optional) (default to 20)

const { status, data } = await apiInstance.getSellerOrdersApiV1SellersOrdersGet(
    page,
    perPage
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] |  | (optional) defaults to 1|
| **perPage** | [**number**] |  | (optional) defaults to 20|


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
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getSellerProductsApiV1SellersProductsGet**
> ProductListResponse getSellerProductsApiV1SellersProductsGet()

Get all products for the current seller

### Example

```typescript
import {
    SellersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let page: number; // (optional) (default to 1)
let perPage: number; // (optional) (default to 20)

const { status, data } = await apiInstance.getSellerProductsApiV1SellersProductsGet(
    page,
    perPage
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] |  | (optional) defaults to 1|
| **perPage** | [**number**] |  | (optional) defaults to 20|


### Return type

**ProductListResponse**

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

# **updateOrderStatusApiV1SellersOrdersOrderIdPut**
> OrderResponse updateOrderStatusApiV1SellersOrdersOrderIdPut(orderUpdate)

Update order status (approve/ship orders)

### Example

```typescript
import {
    SellersApi,
    Configuration,
    OrderUpdate
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let orderId: string; // (default to undefined)
let orderUpdate: OrderUpdate; //

const { status, data } = await apiInstance.updateOrderStatusApiV1SellersOrdersOrderIdPut(
    orderId,
    orderUpdate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orderUpdate** | **OrderUpdate**|  | |
| **orderId** | [**string**] |  | defaults to undefined|


### Return type

**OrderResponse**

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

# **updateProductApiV1SellersProductsProductIdPut**
> ProductResponse updateProductApiV1SellersProductsProductIdPut(productUpdate)

Update a product

### Example

```typescript
import {
    SellersApi,
    Configuration,
    ProductUpdate
} from './api';

const configuration = new Configuration();
const apiInstance = new SellersApi(configuration);

let productId: string; // (default to undefined)
let productUpdate: ProductUpdate; //

const { status, data } = await apiInstance.updateProductApiV1SellersProductsProductIdPut(
    productId,
    productUpdate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **productUpdate** | **ProductUpdate**|  | |
| **productId** | [**string**] |  | defaults to undefined|


### Return type

**ProductResponse**

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

