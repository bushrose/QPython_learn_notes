## 一、QPython安装配置

### 1.1. QPython介绍
QPython是一个可以在安卓设备运行python的脚本引擎。版本有QPython 3L和QPython 3C，3L为官方版本，可以在应用市场搜索下载。3C版本为＂乘着船＂大佬的修改版本。由于3L版本有许多权限限制及很多包不能安装，文章中使用3C版本完成。

### 1.2. 下载地址
百度搜索"QPython 3C开源版"，进入gitee，找到链接即可下载，如下图:
![Screenshot_2023-01-29-14-53-48-450_mark](https://gitee.com/teisyogun/images/raw/master/Screenshot_2023-01-29-14-53-48-450_mark.jpg)

百度网盘下载：`https://pan.baidu.com/s/1zT1NGtYTe55m6bSRWlePRg`
提取码：zxcv

帮助文档：`https://www.bilibili.com/read/cv13322251`

## 二、获取短信内容并生成词云

- **获取短信内容**
获取短信将使用`SL4A` 的api，关于SL4A的介绍及文档，打开第一点gitee中相关链接，如下图：
![Screenshot_2023-01-29-19-35-29-899_mark](https://gitee.com/teisyogun/images/raw/master/Screenshot_2023-01-29-19-35-29-899_mark.jpg)
话不多说，直接上代码：

- **获取所有短信并存入csv**

```python
import androidhelper
import csv

droid=androidhelper.Android()
# 获取短信具体内容并存入csv
def saveSMSToFile(save_path):
    # 获取所有收取的短信。False为获取所有短信，True为获取未读短信；inbox为收件箱，outbox为发件箱
    sms_data=droid.smsGetMessages(False, 'inbox').result
    '''
    id：每条短信的原始id
    address：对方手机号
    date：短信息的时间戳
    body：短信具体内容
    read：已读未读，1为已读，0是未读。
    status不知道是啥
    type，发信息还是收信息，1为收，2为发
    '''
    headers=['_id', 'address', 'date', 'body', 'read', 'status', 'type'] 
    with open(save_path,'w') as f:
        f_scv = csv.DictWriter(f, headers)
        f_scv.writeheader()
        f_scv.writerows(sms_data)
    return save_path
```


- **利用`jieba`分词及`pyecharts`生成词云**

```python

# 停用词，生成词云会过滤，根据实际情况修改
FILTER_WORDS = ['你', '我','他','我们', '他们', ',','验证码',':', '的','账号', 'cn', 'https', '0.00', '点击', '退订', '尊敬','客户', 'TD', '登录','http', '12582', '61.56', '0.42','u.10010', 'http', 'com']


#获取关键词数量，用于词云展示时的数量，num可以修改，词云展示生成时的数量 
def getKeyWordsCounts(filepath, num=30):  
    with open(filepath,'r') as f:  
        f_csv=csv.reader(f)  
        headers=next(f_csv)  
        content=",".join([row[3] for row in f_csv])  
        #print(content)  
        seg_list=list(jieba.cut(content))  
        # print(seg_list)  
         
    keywords_counts = pd.Series(seg_list)  
    keywords_counts = keywords_counts[keywords_counts.str.len()>1]  
    keywords_counts = keywords_counts[~keywords_counts.str.contains('|'.join(FILTER_WORDS))]  
    keywords_counts = keywords_counts.value_counts()[:num]  
    return keywords_counts


# 构建生成词云的元组  
def getWords(keywords_counts):  
    words=[]  
    for i, v in keywords_counts.items():  
        words.append((i,v))  
    return words


# 渲染html  
def render_html(html_filepath,words):  
    c = (  
        WordCloud()  
        .add(  
            "",  
            words,  
            word_size_range=[20, 100],  
            textstyle_opts=opts.TextStyleOpts(font_family="cursive"),  
        )  
        .set_global_opts(title_opts=opts.TitleOpts(title=os.path.splitext(html_filepath)[0]))  
        .render(html_filepath)  
)


# 生成词云  
def genWordCloud(csv_filepath,html_filepath, num=30): csv_filepath=saveSMSToFile(csv_filepath)  
    keywords_counts=getKeyWordsCounts(csv_filepath, num=30)  
    words=getWords(keywords_counts)  
    render_html(html_filepath, words)

```



- **传入文件地址及html地址**

```python
csv_filepath='/storage/emulated/0/0/sms.csv'  
html_filepath='/storage/emulated/0/0/短信词云分析.html'  
genWordCloud(csv_filepath, html_filepath)  
  
# 使用qpython自带的浏览器访问  
jsla('viewHtml', html_filepath)
```

最终实现效果如下图：
![Screenshot_2023-01-29-20-53-24-898_indi](https://gitee.com/teisyogun/images/raw/master/Screenshot_2023-01-29-20-53-24-898_indi.jpg)

完整版代码，点击底部阅读原文，回复【Qpython词云】

## 三、总结
文章采用Sl4A和QPython完成了短信词云生成。`SL4A`提供了丰富的api，如通过QPython结合scikit-learn监测并过滤删除垃圾短信等,这些都由大家自己去探索。

[阅读原文](https://mp.weixin.qq.com/s?__biz=MzIxMTc5NDgzNw==&mid=2247483684&idx=1&sn=ba190cd70891a7bb79d588a9065d8a96&chksm=974eafdea03926c81f3a49c212e379d18e6c82c1fb942d4fc63f3bbd637bd1cad4406ceb4249#rd)