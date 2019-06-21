"""
实例2：读取文件内容发送邮件主体
"""
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
# 导入日志框架
from utils.log import logger

"""
email.mime.text.MIMEText (_text[, _subtype[, _charset]])：
MIMENonMultipart中的一个子类，创建包含文本数据的邮件体，_text 是包含消息负载的字符串，_subtype 指定文本类型，
支持 plain（默认值）或 html类型的字符串。_charset设置字符集，参数接受一个charset实例。
"""
with open('mailfile','rb') as fp:   #读取文件内容
    msg=MIMEText(fp.read(),'plain','utf-8')   #创建消息对象
logger.debug('读取的消息为:{}'.format(msg))

HOST = "mail.woniuxy.com"  # 定义smtp主机
TO = "xulinlin@woniuxy.com"  # 定义邮件收件人
FROM = "student@woniuxy.com"  # 定义邮件发件人
PASSWD = "Student123"  # 定义邮件发送人密码

msg['Subject'] = "测试通过Python发送邮件"
msg['From'] = formataddr(["学生","student@woniuxy.com"])
msg['To'] = formataddr(["徐林林","xulinlin@woniuxy.com"])

# if __name__ == '__main__':
    # try:
    #     server = smtplib.SMTP() # 创建一个 SMTP() 对象
    #     server.connect(HOST,"25") # 通过 connect 方法连接 smtp 主机
    #     #server.starttls() # 启动安全传输模式
    #     server.login(FROM,PASSWD) # 邮箱账号登录校验
    #     server.sendmail(FROM,TO, msg.as_string()) # 邮件发送
    #     server.quit() # 断开 smtp 连接
    #     print("邮件发送成功！")
    # except Exception as e:
    #     print('失败：'+str(e))