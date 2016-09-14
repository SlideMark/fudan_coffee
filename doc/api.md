# 概述

API接口说明

# 错误码

``` 
    SUCCESS = 0
    OPERATE_ERROR = 10001
    DATA_NOT_EXIST = 10002
    AUTH_REQUIRED = 10003
    DUPLICATE_DATA = 10004
    PARAMETER_ERROR = 10005
    LOW_BALANCE = 10006
```

# 登录、注册相关

## GET /account/signin

微信登录，会设置cookie

### Request Path paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code   | y    | string | 微信认证的code |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 用户信息|

#### 用户信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y    | number | 用户的id |
| name  | y     | string | 用户昵称|
| gender | y | number | 性别：0不明，1男，2女|
| province | y | string | 省份|
| city    | y| string |城市|
| avatar | y | string | 头像|
| balance | y | number | 钱包余额|
| coupon |  y | number | 优惠券余额|
| phone | y | number | 电话号码|

## POST /account/login

手机号密码登录，会设置cookie

### Post Body paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| phone   | y    | string | 手机号码 |
| password   | y    | string | 密码 |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 用户信息，同上|

## GET /account/signout

登出

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |

## POST /account/signup

手机号密码注册，会设置cookie

### Post Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| phone   | y    | string | 手机号码 |
| password   | y    | string | 密码 |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 用户信息，同上|

# 用户相关

## GET /user

获取自己的信息

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 用户信息，同上|

# 商品相关

## GET /products

获取商品列表

### Request Path paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| shop_id   | n   | number | 店铺代码，默认0 |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | array | 商品信息列表|

#### 商品信息

| key | Requried | type | description |
|-----|----------|------|-------------|
| id  | y    | number | 商品ID |
| name  | y     | string | 商品名称|
| description | y| string | 商品描述|
| icon | y| string | 商品图标|
| shop_id | y | number | 所属店铺ID| 
| price | y | number| 价格，单位分|
| create_at| y| string | 创建时间|
| update_at | y | string | 更新时间| 

## GET /product/{product_id}

获取单个商品

### URL paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| product_id   | n   | number | 商品ID |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 商品信息， 同上|

## GET /product/{product_id}/with_balance

使用余额购买单个商品

### URL paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| product_id   | n   | number | 商品ID |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 商品信息， 同上|

## GET /product/{product_id}/with_coupon

使用余额购买单个商品

### URL paramater说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| product_id   | n   | number | 商品ID |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 商品信息， 同上|

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

获取充值商品信息

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
| id  | y    | number | 购物车ID |
| name | y| string | 商品名|
| money | y | number | 金额|
| description| y | string | 描述|
| charge| y | number | 返现金额|
| create_at| y| string | 创建时间|
| update_at | y | string | 更新时间| 


'appid': self.appid,
                        'partnerid': config.WX_MCH_ID,
                        'prepayid': response.get('prepay_id'),
                        'package': 'Sign=WXPay',
                        'noncestr': response.get('nonce_str'),
                        'timestamp': str(int(time.time()))
                    }
                    resp['sign'] = PayOrder.sign(resp, self.pay_way)
                    resp['payment_id'] = self.pw_tid

