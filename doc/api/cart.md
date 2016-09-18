
# 购物车相关

## GET /cart

查询购物车内物品

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | array | 购物车信息列表|

#### 购物车信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y    | number | 购物车ID |
| uid  | y     | number | 用户id|
| product | y| number | 商品id|
| product_name| y | string | 商品名称|
| product_price| y | number | 商品价格，分|
| num | y | number| 数量|
| create_at| y| string | 创建时间|
| update_at | y | string | 更新时间| 

## POST /cart

加入购物车

### Post Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| product_id   | y    | number | 商品ID |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |

## POST /cart/update

修改购物车

### Post Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| cart_id   | y    | number | 订单ID |
| num | y| number | 数量后的数量|

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data | y | object | cart信息|

## POST /cart/pay_with_balance

余额结算购物车

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data | y | object | 包含success和fail两个属性， 每个属性为一个商品信息列表，商品信息同上|

## POST /cart/pay_with_coupon

余额结算购物车

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data | y | object | 包含success和fail两个属性， 每个属性为一个商品信息列表，商品信息同上|

