# WebhookData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subscription_id** | **string** |  | [default to undefined]
**status** | **string** |  | [default to undefined]
**product_id** | **string** |  | [default to undefined]
**customer** | [**Customer**](Customer.md) |  | [default to undefined]
**metadata** | [**PaymentMetadata**](PaymentMetadata.md) |  | [optional] [default to undefined]
**next_billing_date** | **string** |  | [default to undefined]

## Example

```typescript
import { WebhookData } from './api';

const instance: WebhookData = {
    subscription_id,
    status,
    product_id,
    customer,
    metadata,
    next_billing_date,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
