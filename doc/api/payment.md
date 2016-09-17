
# 充值相关

## GET /payment_items

获取充值商品信息

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | array | 充值商品列表|

#### 充值商品信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y    | number | 购物车ID |
| name | y| string | 商品名|
| money | y | number | 金额|
| description| y | string | 描述|
| charge| y | number | 返现金额|
| create_at| y| string | 创建时间|
| update_at | y | string | 更新时间| 


## POST /payment_item/{item_id}

购买充值商品

### URL Parameter说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| item_id  | y    | number | 充值商品ID |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 充值商品|

#### 充值商品信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y    | number | 购物车ID |
| name | y| string | 商品名|
| money | y | number | 金额|
| description| y | string | 描述|
| charge| y | number | 返现金额|
| create_at| y| string | 创建时间|
| update_at | y | string | 更新时间| 

## POST /payment_order

获取充值商品的微信订单

### URL Parameter说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| item_id  | y    | number | 充值商品ID |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 订单信息|

#### 订单信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y | number | 订单id|
| appid  | y    | string | appid |
| partnerid | y| string | 商户id|
| prepayid | y | string | prepayid|
| package| y | string | package|
| noncestr| y | number | 随机串|
| timestamp| y| string | 时间戳|
| sign | y | string | 签名|
