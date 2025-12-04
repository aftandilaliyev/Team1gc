# AuthenticationApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getMeAuthMeGet**](#getmeauthmeget) | **GET** /auth/me | Get Me|
|[**loginAuthLoginPost**](#loginauthloginpost) | **POST** /auth/login | Login|
|[**registerAuthRegisterPost**](#registerauthregisterpost) | **POST** /auth/register | Register|

# **getMeAuthMeGet**
> UserResponse getMeAuthMeGet()

Get current user information from JWT token.

### Example

```typescript
import {
    AuthenticationApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthenticationApi(configuration);

let xAuthHeader: string; // (default to undefined)

const { status, data } = await apiInstance.getMeAuthMeGet(
    xAuthHeader
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **xAuthHeader** | [**string**] |  | defaults to undefined|


### Return type

**UserResponse**

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

# **loginAuthLoginPost**
> { [key: string]: any; } loginAuthLoginPost(userLogin)

Login with username and password to get access token.

### Example

```typescript
import {
    AuthenticationApi,
    Configuration,
    UserLogin
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthenticationApi(configuration);

let userLogin: UserLogin; //

const { status, data } = await apiInstance.loginAuthLoginPost(
    userLogin
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userLogin** | **UserLogin**|  | |


### Return type

**{ [key: string]: any; }**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **registerAuthRegisterPost**
> UserResponse registerAuthRegisterPost(userCreate)

Register a new user with email, username, and password.

### Example

```typescript
import {
    AuthenticationApi,
    Configuration,
    UserCreate
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthenticationApi(configuration);

let userCreate: UserCreate; //

const { status, data } = await apiInstance.registerAuthRegisterPost(
    userCreate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userCreate** | **UserCreate**|  | |


### Return type

**UserResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

