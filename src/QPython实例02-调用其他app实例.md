## 一、前言
---

使用版本：QPython 3c

下载地址：百度搜索QPython 3C开源版即可下载

或关注【产品经理不是经理】gzh，回复【qpython 3c】即可获取下载链接。


## 二、代码实例
---
**注意**
```python
# 执行以下方法前，请加上以下代码
from androidhelper import Android
droid=Android()
```

### 打开qq群

```python
def jumpQQTeam(qqTeam):
    action="android.intent.action.VIEW"
    uri=f"mqqapi://card/show_pslcard?src_type=internal&version=1&uin={qqTeam}&card_type=group&source=qrcode"
    intent=droid.makeIntent(action=action, uri=uri)
    droid.startActivityIntent(intent.result)
    
```

### 打开qq

```python

def jumpQQ(qq):
    action="android.intent.action.VIEW"
    uri=f"mqqapi://card/show_pslcard?src_type=internal&source=sharecard&version=1&uin={qq}"
    intent=droid.makeIntent(action=action, uri=uri)
    droid.startActivityIntent(intent.result)
```

### 分享纯文本到QQ

```python
def shareQQ(content):
    action="android.intent.action.SEND"
    mime="text/plain"
    extras={
        "android.intent.extra.SUBJECT":"share",
        "android.intent.extra.TEXT":content
    }
    flags=FLAG_ACTIVITY_NEW_TASK
    packageName="com.tencent.mobileqq"
    className="com.tencent.mobileqq.activity.JumpActivity"
    intent=droid.makeIntent(action=action,type=mime,extras=extras,flags=flags,packagename=packageName,classname=className)
    droid.startActivityIntent(intent.result)
```

### 打开浏览器搜索

```python
def search(content):
    # 等同于droid.search(content)
    action="android.intent.action.WEB_SEARCH"
    extras={
        "query":content,
    }
    intent=droid.makeIntent(action=action, extras=extras)
    droid.startActivityIntent(intent.result)
```

### 启动app

```python
# 启动app
def launchAPP(appName):
    flag=False
    # 获取用户安装的app
    #  getInstalledPackages.APPS_ALL = 5  (所有应用)
    #  getInstalledPackages.APPS_USER = 4 (用户应用，默认)
    #  getInstalledPackages.APPS_SYSTEM = 3 (系统应用)
    #  getInstalledPackages.APPS_SYSTEM_UPDATED = 2 (系统已更新应用)
    #  getInstalledPackages.APPS_SYSTEM_NOT_UPDATED = 1 (系统未更新应用)
    installedAPPs=droid.getInstalledPackages(flag=droid.getInstalledPackages.APPS_USER)
    if appName not in installedAPPs.result.values():
        droid.makeToast(f"{appName}未安装")
        return flag
    # 获取可启动包名、类名、应用名
    apps=droid.getLaunchablePackages(True)
    appsInfo=[(k, v.split('|')[0], v.split('|')[1]) for k, v in apps.result.items()]
 
    if appName not in [a[2] for a in appsInfo]:
        droid.makeToast(f"{appName}无权限启动")
        return flag
    packagename=[p[0] for p in appsInfo if p[2] == appName]
    classname=[p[1] for p in appsInfo if p[2] == appName]
    droid.launch(classname=classname[0], packagename=packagename[0], wait=True)
    flag=True
    return flag
```

### 安装app（该方法无法执行，未授权）

```python
FLAG_ACTIVITY_NEW_TASK=268435456
def installAPP(apkPath):
    "无安装其他app权限"
    action="android.intent.action.VIEW"
    uri=droid.pathToUri(apkPath).result
    mime="application/vnd.android.package-archive"
    flags=FLAG_ACTIVITY_NEW_TASK
    intent=droid.makeIntent(action=action,uri=uri,type=mime,flags=flags)
    droid.startActivityIntent(intent.result)
```

### 卸载app

```python
def unInstallAPP(packageName):
    #  
    action="android.intent.action.DELETE"
    uri=f"package:{packageName}"
    intent=droid.makeIntent(action=action,uri=uri)
    droid.startActivityIntent(intent.result)
```

### 拨打电话

```python
def dial(phone):
    action="android.intent.action.CALL"
    uri=f"tel:{phone}"
    intent=droid.makeIntent(action=action,uri=uri)
    droid.startActivityIntent(intent.result)
```

### 打开系统设置

```
ACTION_SETTINGS   android.settings.SETTINGS 
ACTION_BLUETOOTH_SETTINGS     android.settings.BLUETOOTH_SETTINGS
修改成对应字符串即可
字段列表:
ACTION_SETTINGS 系统设置
ACTION_APN_SETTINGS APN设置
ACTION_LOCATION_SOURCE_SETTINGS 位置和访问信息
ACTION_WIRELESS_SETTINGS 网络设置
ACTION_AIRPLANE_MODE_SETTINGS 无线和网络热点设置
ACTION_SECURITY_SETTINGS 位置和安全设置
ACTION_WIFI_SETTINGS 无线网WIFI设置
ACTION_WIFI_IP_SETTINGS 无线网IP设置
ACTION_BLUETOOTH_SETTINGS 蓝牙设置
ACTION_DATE_SETTINGS 时间和日期设置
ACTION_SOUND_SETTINGS 声音设置
ACTION_DISPLAY_SETTINGS 显示设置——字体大小等
ACTION_LOCALE_SETTINGS 语言设置
ACTION_INPUT_METHOD_SETTINGS 输入法设置
ACTION_USER_DICTIONARY_SETTINGS 用户词典
ACTION_APPLICATION_SETTINGS 应用程序设置
ACTION_APPLICATION_DEVELOPMENT_SETTINGS 应用程序设置
ACTION_QUICK_LAUNCH_SETTINGS 快速启动设置
ACTION_MANAGE_APPLICATIONS_SETTINGS 已下载（安装）软件列表
ACTION_SYNC_SETTINGS 应用程序数据同步设置
ACTION_NETWORK_OPERATOR_SETTINGS 可用网络搜索
ACTION_DATA_ROAMING_SETTINGS 移动网络设置
ACTION_INTERNAL_STORAGE_SETTINGS 手机存储设置
```

```python
def startSettings(action="android.settings.SETTINGS"):
    droid.startActivity(action=action)
```

### 打开文件

``` python
FLAG_ACTIVITY_NEW_TASK=268435456
def openFile(path):
    action="android.intent.action.VIEW"
    uri=droid.pathToUri(path).result
    flags=FLAG_ACTIVITY_NEW_TASK
    intent=droid.makeIntent(action=action,uri=uri, flags=flags)
    droid.startActivityIntent(intent.result)
```

### 调用文件管理器选择图片

```python
# 调用文件选择器选择图片
def pickPic():
    action="android.intent.action.PICK"
    mime="images/*"
    packagename="com.android.fileexplorer"
    classname="com.android.fileexplorer.activity.FileActivity"
    #intent=droid.makeIntent(action=action,type=mime, packagename=packagename, classname=classname)
    #f=droid.startActivityForResultIntent(intent.result)
    f=droid.startActivityForResult(action=action,type=mime, packagename=packagename, classname=classname)
    return f.result
```

### 发送短信

```python
def smsSend(message, phone):
    action="android.intent.action.SENDTO"
    uri=f"smsto:{phone}"
    extras={
        "sms_body":message
    }
    action="android.intent.action.VIEW"
    droid.startActivity(action=action,uri=uri, extras=extras)
```

### 返回桌面

```python
def backHome():
    action="android.intent.action.MAIN"
    categories=["android.intent.category.HOME"]
    intent=droid.makeIntent(action=action, categories=categories)
    droid.startActivityIntent(intent.result)
```

## 三、总结

文章中实例均采用qpython 3c自带sl4a完成，sl4a为提供了丰富的api和安卓交互，更多实例由大家自行探索。