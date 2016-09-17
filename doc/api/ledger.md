
# 消费记录相关

## GET /ledgers

获取消费记录

### Request Path paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| type   | y    | number | 类型，0：余额记录，1：优惠券记录 |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | array | 消费记录的列表|

#### 消费记录信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y    | number | 购物车ID |
| uid  | y     | number | 用户id|
| name | y| string | 商品名|
| money | y | number | 金额|
| type| y | string | 记录类型|
| item_id| y | number | 商品id|
| create_at| y| string | 创建时间|
| update_at | y | string | 更新时间| 
