# CheckoutRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_address** | **string** |  | [default to undefined]
**billing_address** | **string** |  | [optional] [default to undefined]
**payment_method** | **string** |  | [optional] [default to 'dodo_payments']

## Example

```typescript
import { CheckoutRequest } from './api';

const instance: CheckoutRequest = {
    shipping_address,
    billing_address,
    payment_method,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
