# ProductResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **string** |  | [default to undefined]
**price** | **string** |  | [default to undefined]
**description** | **string** |  | [optional] [default to undefined]
**stock_quantity** | **number** |  | [optional] [default to 0]
**id** | **string** |  | [default to undefined]
**seller_id** | **number** |  | [default to undefined]
**product_type** | **string** |  | [optional] [default to undefined]
**created_at** | **string** |  | [default to undefined]
**updated_at** | **string** |  | [default to undefined]
**images** | [**Array&lt;ProductImageResponse&gt;**](ProductImageResponse.md) |  | [optional] [default to undefined]

## Example

```typescript
import { ProductResponse } from './api';

const instance: ProductResponse = {
    name,
    price,
    description,
    stock_quantity,
    id,
    seller_id,
    product_type,
    created_at,
    updated_at,
    images,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
