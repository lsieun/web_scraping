# IGETGET #

借助于mitmweb，爬取得到App内容

## 功能列表 ##

- [x]01：從mitmproxy中讀取Headers信息
- [x]02：統計App訪問URL的次數
- [x]03：获取栏目的内容
- [x]04：获取课程的内容
- [ ]05：获取电子书的列表
- [ ]06：获取笔记的列表

## 反思 ##

查看apk文件源的误区：

**第01次**：计算header中的G-Auth-Sign时

起先，是被`localObject1 = "text/plain";`所迷惑，认为只是普通的字符串
后来，发现原来这里应该表示实际的Request中的Content-Type，它的值或者为“application/x-www-form-urlencoded”或者为“application/json”。

**第02次**：计算url中的sign时

```
    Object localObject = new HashMap();
    ((HashMap)localObject).put("token", paramString);
    localObject = a.a("dc923c14b6419aca91d8bb1e2e5e35e4", (HashMap)localObject);
```

起先，认为hashmap中只存放了"token"，一直认为是"dc923c14b6419aca91d8bb1e2e5e35e4"有错误，这可能是受第01次的影响
后来，经过不断尝试，发现hashmap中存在两个值，一个是"token"，另一个是"appid"


