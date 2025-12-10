# UploadsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**deleteImageApiV1UploadsImageFileKeyDelete**](#deleteimageapiv1uploadsimagefilekeydelete) | **DELETE** /api/v1/uploads/image/{file_key} | Delete Image|
|[**getImageUrlApiV1UploadsImageFileKeyUrlGet**](#getimageurlapiv1uploadsimagefilekeyurlget) | **GET** /api/v1/uploads/image/{file_key}/url | Get Image Url|
|[**uploadImageApiV1UploadsImagePost**](#uploadimageapiv1uploadsimagepost) | **POST** /api/v1/uploads/image | Upload Image|
|[**uploadMultipleImagesApiV1UploadsImagesPost**](#uploadmultipleimagesapiv1uploadsimagespost) | **POST** /api/v1/uploads/images | Upload Multiple Images|

# **deleteImageApiV1UploadsImageFileKeyDelete**
> any deleteImageApiV1UploadsImageFileKeyDelete()

Delete an image from R2 bucket.

### Example

```typescript
import {
    UploadsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UploadsApi(configuration);

let fileKey: string; // (default to undefined)

const { status, data } = await apiInstance.deleteImageApiV1UploadsImageFileKeyDelete(
    fileKey
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **fileKey** | [**string**] |  | defaults to undefined|


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

# **getImageUrlApiV1UploadsImageFileKeyUrlGet**
> any getImageUrlApiV1UploadsImageFileKeyUrlGet()

Get public URL for an image.

### Example

```typescript
import {
    UploadsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UploadsApi(configuration);

let fileKey: string; // (default to undefined)

const { status, data } = await apiInstance.getImageUrlApiV1UploadsImageFileKeyUrlGet(
    fileKey
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **fileKey** | [**string**] |  | defaults to undefined|


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

# **uploadImageApiV1UploadsImagePost**
> any uploadImageApiV1UploadsImagePost()

Upload a single image to R2 bucket.

### Example

```typescript
import {
    UploadsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UploadsApi(configuration);

let file: File; // (default to undefined)
let path: string; // (optional) (default to 'images')

const { status, data } = await apiInstance.uploadImageApiV1UploadsImagePost(
    file,
    path
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **file** | [**File**] |  | defaults to undefined|
| **path** | [**string**] |  | (optional) defaults to 'images'|


### Return type

**any**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uploadMultipleImagesApiV1UploadsImagesPost**
> any uploadMultipleImagesApiV1UploadsImagesPost()

Upload multiple images to R2 bucket.

### Example

```typescript
import {
    UploadsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UploadsApi(configuration);

let files: Array<File>; // (default to undefined)
let path: string; // (optional) (default to 'images')

const { status, data } = await apiInstance.uploadMultipleImagesApiV1UploadsImagesPost(
    files,
    path
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **files** | **Array&lt;File&gt;** |  | defaults to undefined|
| **path** | [**string**] |  | (optional) defaults to 'images'|


### Return type

**any**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

