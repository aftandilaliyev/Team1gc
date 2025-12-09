# ProductCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **string** |  | [default to undefined]
**price** | [**Price**](Price.md) |  | [default to undefined]
**description** | **string** |  | [optional] [default to undefined]
**stock_quantity** | **number** |  | [optional] [default to 0]
**product_type** | **string** |  | [optional] [default to undefined]
**images** | [**Array&lt;ProductImageCreate&gt;**](ProductImageCreate.md) |  | [optional] [default to undefined]

## Example

```typescript
import { ProductCreate } from './api';

const instance: ProductCreate = {
    name,
    price,
    description,
    stock_quantity,
    product_type,
    images,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
