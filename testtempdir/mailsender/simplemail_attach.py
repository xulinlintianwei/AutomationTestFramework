"""
实例2：读取文件内容发送邮件主体
"""
import smtplib
from email.utils import formataddr
from email.mime.base import MIMEBase  #MIME子类的基类
from email import encoders   #导入编码器
# 处理附件
from email.mime.multipart import MIMEMultipart
"""
email.mime.multipart.MIMEMultipart（_subtype='mixed'，boundary= None，_subparts = None，*，policy = compat32，** _ params )：
作用是生成包含多个部分的邮件体的 MIME 对象，参数 _subtype 指定要添加到"Content-type:multipart/subtype" 报头的可选的三种子类型，
分别为 mixed、related、alternative，默认值为 mixed。定义 mixed实现构建一个带附件的邮件体；定义related 实现构建内嵌资源的邮件体；定义alternative 则实现构建纯文本与超文本共存的邮件体；_subparts是有效负载的一系类初始部分，可以使用attach()方法将子部件附加到消息中。
"""

# 导入日志框架
from utils.log import logger

# msg1 = MIMEMultipart('mixed')  #创建带附件的实例
# msg2 = MIMEMultipart('related')  #创建内嵌资源的实例
# msg3 = MIMEMultipart('alternative') #创建纯文本与超文本实例

"""
email.mime.text.MIMEText (_text[, _subtype[, _charset]])：
MIMENonMultipart中的一个子类，创建包含文本数据的邮件体，_text 是包含消息负载的字符串，_subtype 指定文本类型，
支持 plain（默认值）或 html类型的字符串。_charset设置字符集，参数接受一个charset实例。
"""
msg = MIMEMultipart('mixed')  #创建带附件的实例
filename = 'project.pdf'
attachfile_base = MIMEBase('application', 'octet-stream')  #创建基础对象指定类型
attachfile_base.set_payload(open(filename,'rb').read())  #设置我有效负载
attachfile_base.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', filename) )
encoders.encode_base64(attachfile_base)
msg.attach(attachfile_base)

HOST = "mail.woniuxy.com"  # 定义smtp主机
TO = "xulinlin@woniuxy.com"  # 定义邮件收件人
FROM = "student@woniuxy.com"  # 定义邮件发件人
PASSWD = "Student123"  # 定义邮件发送人密码

msg['Subject'] = "测试通过Python发送邮件"
msg['From'] = formataddr(["学生","student@woniuxy.com"])
msg['To'] = formataddr(["徐林林","xulinlin@woniuxy.com"])

if __name__ == '__main__':
    try:
        server = smtplib.SMTP() # 创建一个 SMTP() 对象
        server.connect(HOST,"25") # 通过 connect 方法连接 smtp 主机
        #server.starttls() # 启动安全传输模式
        server.login(FROM,PASSWD) # 邮箱账号登录校验
        server.sendmail(FROM,TO, msg.as_string()) # 邮件发送
        server.quit() # 断开 smtp 连接
        print("邮件发送成功！")
    except Exception as e:
        print('失败：'+str(e))