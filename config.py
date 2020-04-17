import os

SECRET_KEY = os.urandom(24)

DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/wlmooe"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True

TEACHER_ID = 'ASDEFAYTJFDHB'
STUDENT_ID = 'ASFASFASFEWGF1564616036'

# 邮箱配置
# 邮箱服务器
MAIL_SERVER = 'smtp.qq.com'
# 端口,qq邮箱不支持非加密方式发送邮件
# TLS端口号是587，SSL端口号是465
MAIL_PORT = '587'
# 是否使用TLS
MAIL_USE_TLS = True
# 是否使用SSL
# MAIL_USE_SSL: default False
# 是否为DEBUG模式，打印调试消息
# MAIL_DEBUG: default app.debug
# 用户名，填邮箱
MAIL_USERNAME = "2413357360@qq.com"
# 密码，填授权码
MAIL_PASSWORD = "ghsnqpxaneujdjdg"
# # 默认发送者，填邮箱
MAIL_DEFAULT_SENDER = "2413357360@qq.com"
# 一次连接中的发送邮件的上限
# MAIL_MAX_EMAILS: default None、
# 设置是否真的发送邮件，True不发送
# MAIL_SUPPRESS_SEND: default app.testing
# 如果 MAIL_ASCII_ATTACHMENTS 设置成 True 的话，
# 文件名将会转换成 ASCII 的。一般用于添加附件。
# MAIL_ASCII_ATTACHMENTS: default False

# 阿里大于相关配置
ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = '小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'

# UEditor的相关配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "fOsvSI_ByPLM_g5ueTBcRfkpX-UjgNs2tJzsbCev"
UEDITOR_QINIU_SECRET_KEY = "b8VMy-_qxHFWDl7zSMunteWhaF9jELvjM9SdHN7S"
UEDITOR_QINIU_BUCKET_NAME = "wanglei1998"
UEDITOR_QINIU_DOMAIN = "q8apk1mqn.bkt.clouddn.com"

# flask-paginate的相关配置
PER_PAGE = 10
