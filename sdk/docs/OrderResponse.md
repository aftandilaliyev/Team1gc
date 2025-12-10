# OrderResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**OrderStatus**](OrderStatus.md) |  | [optional] [default to undefined]
**id** | **string** |  | [default to undefined]
**user_id** | **number** |  | [default to undefined]
**total_amount** | **number** |  | [default to undefined]
**shipping_address** | **string** |  | [optional] [default to undefined]
**billing_address** | **string** |  | [optional] [default to undefined]
**created_at** | **string** |  | [default to undefined]
**updated_at** | **string** |  | [default to undefined]
**items** | [**Array&lt;OrderItemResponse&gt;**](OrderItemResponse.md) |  | [optional] [default to undefined]

## Example

```typescript
import { OrderResponse } from './api';

const instance: OrderResponse = {
    status,
    id,
    user_id,
    total_amount,
    shipping_address,
    billing_address,
    created_at,
    updated_at,
    items,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
