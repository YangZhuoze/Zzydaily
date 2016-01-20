# Zzydaily
A blog deployed on SAE -> yangzhuoze.applinzi.com

# 账号
登陆只能使用新浪微博进行登陆，如果是第一次登陆会根据微博用户资料来生成站内用户资料。默认生成的用户权限为只能进行评论。

# 文章
新发表文章逻辑处理顺序：
    1、判断是否具有发表文章的权限，在View和Control分别判断，一个为了引导，一个为了防止通过直接控制Http来进行发表。
    2、获取文章标题，清楚所有HTML格式。
    3、获取文章富文本、作者为当前登陆用户、目录、时间戳
    4、生成文章预览：
        a、获取内容第一个img标签。
        b、清除除了['b', 'i', 'y', 'strike']以外的所有标签。
        c、切片截取前N个字符。
        d、补全缺少的关闭标签。
        e、偷懒跳过上面所有步骤

前端文章预览：没有进行文章预览裁剪。单行文本溢出显示省略号CSS：text-overflow:ellipsis;对于多行文本无效。要实现多行文本溢出裁剪需要用到WebKit的CSS：display: -webkit-box; -webkit-box-orient; text-overflow: ellipsis; 由于用了之后我又出现了新的问题（带图片的预览文本部分无法显示）于是决定放弃…直接使用限定128个字符文章预览裁剪