[toc]

# Cookie
【Cookie产生背景】
1. Http是一种无状态的协议，客户端向服务器请求，服务器无论你是谁，你是第几次访问，都返回给你同样的东西
2. 【需求】正因为客户端是一种无状态的请求，那每次请求都需要登录一次，每一次都需要输入账号密码很麻烦。产生了cookie

【Cookie工作机制】
1. Cookie存储在本地
2. 是一种浏览器的行为
3. 用户每次请求时都将id一起给服务器，服务器就知道你的状态

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190129091109142.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

# Session
【Session产生背景】浏览器把用户账号、密码、ID都以明文的形式存在Cookie中，有很大的安全隐患

【Session工作机制】
1. 用户首次请求服务
2. 服务器发现他没有带回SessionID
3. 服务器为该用户创建Session，并为其随机生成一个字符串SessionID，并将其账号密码等信息以加密的形式，搞成一个字符串存储在本地，传回SessionID给浏览器
4. 浏览器将SessionID存在Cookie

# 常见httpcode

|code|说明|
|-|-|
|200|请求被成功处理|
|301/302|永久性重定向/临时性重定向|
|403|没有权限访问|
|404|表示没有对应的资源|
|500|服务器错误|
|503|服务器停机或正在维护|

# 模拟登陆
【前期工作】
1. 通过错误的账号来分析登陆界面
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190129113909643.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
2. 检查用其他方法登陆（邮箱、手机等），是不是另一个url

【模拟登陆】
1. 【如何取到_xsrf】请求登录界面，可以解析到此次的_xsrf
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190129114157685.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
2. 【做post】拿到_xsrf做post --> 服务器会返回cookie（说明：你下一次登录要将哪些值带过来）
3. 【保存cookie】
4. 【再次请求】下一次请求时把cookie带过去 