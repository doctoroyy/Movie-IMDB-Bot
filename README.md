<p align="center">
  <a href="https://vika.cn/share/shruZUUMv38WYu9ywJeX1"><img src="https://s1.vika.cn/space/2021/04/03/26cf3d796c034d6aa3c50995b11338eb?attname=image.png" alt="Movie IMDB Bot" /></a>
</p>

# Movie IMDB Bot
一个为电影爱好者获取 IMDB TOP 250 中英文对照信息的自动化工具.

# Get Started

### 1. [注册维格表帐户](https://vika.cn/?inviteCode=28762276), 将 [互联网影视数据库](https://vika.cn/share/shrG4k0oxQCgCa4ggnptS) 保存为模板.

### 2. fork 这个项目, 在 Setings 中依次创建如下 secrets key (*VIKA_API_TOKEN*, *DATASHEET_ID*, *SHARING_DST_ID*,  *TOP_VIEW_ID*)
   
<img src="https://s1.vika.cn/space/2021/04/03/518d3caf12eb4304be1c6c814836cc27?attname=image.png" />

- VIKA_API_TOKEN
  <img src="https://s1.vika.cn/space/2021/04/03/f19f2df18393406d92a738a436dceac2?attname=image.png" />
  
- DATASHEET_ID、SHARING_DST_ID
  <img src="https://s1.vika.cn/space/2021/04/03/9abafe7ba53d4d4d86b936c6855739d2?attname=image.png" />
  打开已经保存到空间站的 互联网影视数据库 文件夹，打开 IMDB 这张表，浏览器地址栏中 /workbench/{dstId}/{viewId} 找到 datasheet_id, 由于我们要操作 2 张表，SHARING_DST_ID 在文件夹下的 IMDB TOP 250 电影榜单 表中获取
  
- TOP_VIEW_ID
  打开 IMDB 这张表，切换到视图 "TOP 250", 复制 viewId (地址栏路径含义为 /workbench/{dstId}/{viewId})
  
至此，我们就做完所有准备工作了。
  
# Use it
在 .github/workflows/bot.yml 文件中，我们定义了事件触发的方式 schedule 可以设置定时触发，
这里初始设置成了每天北京时间 07:00 开始执行任务。
另外，有任何更改被 push 到 master 分支时，也会触发这个任务。如果你想手动触发，可以随意更改 README.md 触发事件
关于 GitHub Action 的更多用法可以参考 [官方文档](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows)

```yaml
on:
  schedule:
    - cron: '0 23 * * *'
  push:
    branches: [ master ]
```
这里附上一个[演示视频](https://s1.vika.cn/space/2021/04/03/5dc50dc4f9ac4bc4aa58c02b7c3d58ec?attname=Kapture%202021-04-03%20at%2021.11.43.mp4)
视频中为了演示，我把模板中表格的数据清空了，实际上我们并不用这样。当在 IMDB 官网查到一条不在数据表中的电影时，Python 脚本会使用 IMDB 号作为关键字在豆瓣上查询电影信息，默认查询时间间隔为 8s，所以看到插入新数据慢的情况并不是卡顿（间隔时间如果设置太短很容易被豆瓣封禁）
<img src="https://s1.vika.cn/space/2021/04/03/90f32e6893e04a1d9a35ade25ba4775e?attname=Kapture%202021-04-03%20at%2020.59.49.gif" />
