# ProductsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getProductApiV1ProductsProductIdGet**](#getproductapiv1productsproductidget) | **GET** /api/v1/products/{product_id} | Get Product|
|[**getProductsApiV1ProductsGet**](#getproductsapiv1productsget) | **GET** /api/v1/products/ | Get Products|

# **getProductApiV1ProductsProductIdGet**
> ProductResponse getProductApiV1ProductsProductIdGet()

Get a single product by ID

### Example

```typescript
import {
    ProductsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProductsApi(configuration);

let productId: string; // (default to undefined)

const { status, data } = await apiInstance.getProductApiV1ProductsProductIdGet(
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

# **getProductsApiV1ProductsGet**
> ProductListResponse getProductsApiV1ProductsGet()

Get paginated list of products with filtering

### Example

```typescript
import {
    ProductsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProductsApi(configuration);

let page: number; // (optional) (default to 1)
let elements: number; // (optional) (default to 20)
let priceMin: number; // (optional) (default to undefined)
let priceMax: number; // (optional) (default to undefined)
let productType: string; // (optional) (default to undefined)
let sort: string; // (optional) (default to 'created_at')
let search: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.getProductsApiV1ProductsGet(
    page,
    elements,
    priceMin,
    priceMax,
    productType,
    sort,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] |  | (optional) defaults to 1|
| **elements** | [**number**] |  | (optional) defaults to 20|
| **priceMin** | [**number**] |  | (optional) defaults to undefined|
| **priceMax** | [**number**] |  | (optional) defaults to undefined|
| **productType** | [**string**] |  | (optional) defaults to undefined|
| **sort** | [**string**] |  | (optional) defaults to 'created_at'|
| **search** | [**string**] |  | (optional) defaults to undefined|


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

