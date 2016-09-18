
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


## POST /account/bindphone

绑定手机号

### Post Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| phone   | y    | string | 手机号码 |

### Response Body说明

| key | Requried | type | description |
|-----|----------|------|-------------|
| code  | y    | number | 返回状态码 |
| data  | y     | object | 用户信息，同上|


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
