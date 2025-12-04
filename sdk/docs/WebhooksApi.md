# WebhooksApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**handleDodoPaymentWebhookApiV1WebhooksDodoPaymentsPost**](#handledodopaymentwebhookapiv1webhooksdodopaymentspost) | **POST** /api/v1/webhooks/dodo-payments | Handle Dodo Payment Webhook|

# **handleDodoPaymentWebhookApiV1WebhooksDodoPaymentsPost**
> any handleDodoPaymentWebhookApiV1WebhooksDodoPaymentsPost(webhookRequest)

Handle DodoPayments webhook events

### Example

```typescript
import {
    WebhooksApi,
    Configuration,
    WebhookRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

let xSignature: string; // (default to undefined)
let webhookRequest: WebhookRequest; //

const { status, data } = await apiInstance.handleDodoPaymentWebhookApiV1WebhooksDodoPaymentsPost(
    xSignature,
    webhookRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **webhookRequest** | **WebhookRequest**|  | |
| **xSignature** | [**string**] |  | defaults to undefined|


### Return type

**any**

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

