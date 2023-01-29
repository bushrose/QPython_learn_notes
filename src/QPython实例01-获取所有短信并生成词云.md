## 一、QPython安装配置

### 1.1. QPython介绍
QPython是一个可以在安卓设备运行python的脚本引擎。版本有QPython 3L和QPython 3C，3L为官方版本，可以在应用市场搜索下载。3C版本为＂乘着船＂大佬的修改版本。由于3L版本有许多权限限制及很多包不能安装，文章中使用3C版本完成。

### 1.2. 下载地址
百度搜索"QPython 3C开源版"，进入gitee，找到链接即可下载，如下图:
![Screenshot_2023-01-29-14-53-48-450_mark](https://gitee.com/teisyogun/images/raw/master/Screenshot_2023-01-29-14-53-48-450_mark.jpg)

百度网盘下载：`https://pan.baidu.com/s/1zT1NGtYTe55m6bSRWlePRg`
提取码：zxcv

帮助文档：`https://www.bilibili.com/read/cv13322251`

### 二、获取短信内容并生成词云

- **获取短信内容**
获取短信将使用`SL4A` 的api，关于SL4A的介绍及文档，打开第一点gitee中相关链接，如下图：
![Screenshot_2023-01-29-19-35-29-899_mark](https://gitee.com/teisyogun/images/raw/master/Screenshot_2023-01-29-19-35-29-899_mark.jpg)
话不多说，直接上代码：
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

**利用就`jieba`分词及`pyecharts`生成词云**

```python
#获取关键词数量，用于词云展示时的数量  
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
def genWordCloud(csv_filepath, html_filepath, num=30):  
    csv_filepath=saveSMSToFile(csv_filepath)  
    keywords_counts=getKeyWordsCounts(csv_filepath, num=30)  
    words=getWords(keywords_counts)  
    render_html(html_filepath, words)

```

