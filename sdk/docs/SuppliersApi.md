# SuppliersApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**approveOrderApiV1SuppliersOrdersOrderIdApprovePost**](#approveorderapiv1suppliersordersorderidapprovepost) | **POST** /api/v1/suppliers/orders/{order_id}/approve | Approve Order|
|[**getAllOrdersApiV1SuppliersOrdersGet**](#getallordersapiv1suppliersordersget) | **GET** /api/v1/suppliers/orders | Get All Orders|
|[**getOrderApiV1SuppliersOrdersOrderIdGet**](#getorderapiv1suppliersordersorderidget) | **GET** /api/v1/suppliers/orders/{order_id} | Get Order|
|[**getOrdersForApprovalApiV1SuppliersOrdersPendingGet**](#getordersforapprovalapiv1suppliersorderspendingget) | **GET** /api/v1/suppliers/orders/pending | Get Orders For Approval|
|[**getSupplierAnalyticsApiV1SuppliersAnalyticsGet**](#getsupplieranalyticsapiv1suppliersanalyticsget) | **GET** /api/v1/suppliers/analytics | Get Supplier Analytics|
|[**updateOrderStatusApiV1SuppliersOrdersOrderIdPut**](#updateorderstatusapiv1suppliersordersorderidput) | **PUT** /api/v1/suppliers/orders/{order_id} | Update Order Status|

# **approveOrderApiV1SuppliersOrdersOrderIdApprovePost**
> OrderResponse approveOrderApiV1SuppliersOrdersOrderIdApprovePost()

Approve an order (move from confirmed to shipped)

### Example

```typescript
import {
    SuppliersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SuppliersApi(configuration);

let orderId: string; // (default to undefined)

const { status, data } = await apiInstance.approveOrderApiV1SuppliersOrdersOrderIdApprovePost(
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

# **getAllOrdersApiV1SuppliersOrdersGet**
> Array<OrderResponse> getAllOrdersApiV1SuppliersOrdersGet()

Get all orders (suppliers can view all orders)

### Example

```typescript
import {
    SuppliersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SuppliersApi(configuration);

let page: number; // (optional) (default to 1)
let perPage: number; // (optional) (default to 20)

const { status, data } = await apiInstance.getAllOrdersApiV1SuppliersOrdersGet(
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

# **getOrderApiV1SuppliersOrdersOrderIdGet**
> OrderResponse getOrderApiV1SuppliersOrdersOrderIdGet()

Get specific order details

### Example

```typescript
import {
    SuppliersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SuppliersApi(configuration);

let orderId: string; // (default to undefined)

const { status, data } = await apiInstance.getOrderApiV1SuppliersOrdersOrderIdGet(
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

# **getOrdersForApprovalApiV1SuppliersOrdersPendingGet**
> Array<OrderResponse> getOrdersForApprovalApiV1SuppliersOrdersPendingGet()

Get orders that need supplier approval

### Example

```typescript
import {
    SuppliersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SuppliersApi(configuration);

let page: number; // (optional) (default to 1)
let perPage: number; // (optional) (default to 20)

const { status, data } = await apiInstance.getOrdersForApprovalApiV1SuppliersOrdersPendingGet(
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

# **getSupplierAnalyticsApiV1SuppliersAnalyticsGet**
> any getSupplierAnalyticsApiV1SuppliersAnalyticsGet()

Get supplier analytics dashboard data

### Example

```typescript
import {
    SuppliersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new SuppliersApi(configuration);

const { status, data } = await apiInstance.getSupplierAnalyticsApiV1SuppliersAnalyticsGet();
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

# **updateOrderStatusApiV1SuppliersOrdersOrderIdPut**
> OrderResponse updateOrderStatusApiV1SuppliersOrdersOrderIdPut(orderUpdate)

Update order status (ship, deliver, cancel)

### Example

```typescript
import {
    SuppliersApi,
    Configuration,
    OrderUpdate
} from './api';

const configuration = new Configuration();
const apiInstance = new SuppliersApi(configuration);

let orderId: string; // (default to undefined)
let orderUpdate: OrderUpdate; //

const { status, data } = await apiInstance.updateOrderStatusApiV1SuppliersOrdersOrderIdPut(
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

