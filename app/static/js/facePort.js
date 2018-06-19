var request = require('request');
var url = require('url');
var crypto = require('crypto');
var date = new Date().toUTCString()
// 这里填写AK和请求
var ak_id = 'NNV..........5jv';
var ak_secret = 'FGs.....................3Zu';
var options = {
    url : 'https://shujuapi.aliyun.com/org_code/service_code/api_name?param1=xxx&param2=xxx',
    method: 'GET',
    body: '',
    headers: {
        'accept': 'application/json',
        'content-type': 'application/json',
        'date': date,
        'Authorization': ''
    }
};
// 这里填写AK和请求
md5 = function(buffer) {
    var hash;
    hash = crypto.createHash('md5');
    hash.update(buffer);
    return hash.digest('base64');
};
sha1 = function(stringToSign, secret) {
    var signature;
    return signature = crypto.createHmac('sha1', secret).update(stringToSign).digest().toString('base64');
};
// step1: 组stringToSign [StringToSign = #{method}\\n#{accept}\\n#{data}\\n#{contentType}\\n#{date}\\n#{action}]
var body = options.body || '';
var bodymd5;
if(body === void 0 || body === ''){
    bodymd5 = body;
} else {
    bodymd5 = md5(new Buffer(body));
}
console.log(bodymd5)
var stringToSign = options.method + "\n" + options.headers.accept + "\n" + bodymd5 + "\n" + options.headers['content-type'] + "\n" + options.headers.date + "\n" + url.parse(options.url).path;
console.log("step1-Sign string:", stringToSign);
// step2: 加密 [Signature = Base64( HMAC-SHA1( AccessSecret, UTF-8-Encoding-Of(StringToSign) ) )]
var signature = sha1(stringToSign, ak_secret);
// console.log("step2-signature:", signature);
// step3: 组authorization header [Authorization =  Dataplus AccessKeyId + ":" + Signature]
var authHeader = "Dataplus " + ak_id + ":" + signature;
console.log("step3-authorization Header:", authHeader);
options.headers.Authorization = authHeader;
console.log('authHeader', authHeader);
// step4: send request
function callback(error, response, body) {
    if (error) {
        console.log("error", error)
    }
    console.log("step4-response body:", response.statusCode, body)
}
request(options, callback);