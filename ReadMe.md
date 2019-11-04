# ReadMe

## CA

系统初始化时会生成一个根CA，该CA是离线的，由根CA对二级CA(sub_CA)发布证书，二级CA在对各用户发布证书。

CA 主要需要实现的功能有：二级CA申请（包括私钥加密的密钥，CA信息），对用户证书请求签名，吊销证书（并存储到吊销数据库），证书列表（并对列表里的所有证书进行备份）。

CA系统只有二级CA管理员能够进入。

### 数据库说明

#### 证书数据库
(暂定)
* id, int类型, 证书id
* serial_number, text类型, 表示证书的序列号/公钥
* state, int类型, 表示证书的状态，预定0表示证书吊销，1表示证书正常，2表示证书过期
* create_date, DATE类型, 证书的创建日期
* effective_time, int类型, 表示证书的有效期, 年为单位
* country, province, city, organization, name等为text类型
* email为text类型

#### 吊销证书数据库

* id, int类型, 证书id
* serial_number, text类型, 表示证书的序列号/公钥
* state, int类型, 表示证书的状态，预定0表示证书吊销，1表示证书正常，2表示证书过期
* create_date, DATE类型, 证书的创建日期
* effective_time, int类型, 表示证书的有效期, 年为单位
* destroy_date, DATE类型, 表示证书的吊销日期
* country, province, city, organization, name等为text类型
* email为text类型


## Client

Client 需要实现的功能有：证书请求生成，获取证书列表，吊销证书。

Client和二级CA之间需要有通信实现证书的传输。

## OpenSSL

OpenSSL 1.1.1 版本支持国密，不过经过我验证生成的证书仍然是基于 Sha256的，生成国密证书这里可能还需要调研。
