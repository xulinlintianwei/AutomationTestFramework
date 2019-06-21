"""
实例1实现简单邮件发送：
SMTP类方法：
SMTP.connect(host='localhost',port=0)　：链接到远程SMTP主机的方法，host为远程主机地址，port为远程主机smtp端口，默认为25，
也可以直接使用host:port形式来表示：如：SMTP.connect('smtp.163.com','25')
SMTP.login(user,password)：登陆需要认证的SMTP服务器，参数为用户名与密码，如SMTP.login('python@163.com','123')
SMTP.sendmail(from_addr,to_addrs,msg,mail_options=[],rcpt_options=[])：实现邮件的发送功能，参数from_addr为发件人，
to_addrs为收件人，msg为邮件内容，如：SMTP.sendmail('python@163.com','demo@qq.com',body)。
SMTP.starttls(keyfile=None,certfile=None)：启用TLS安全传输模式，所有SMTP指令都将加密传输，如使用gmail的smtp服务时需哟啊
启动此项才能正常发送邮件。
SMTP.quit()：断开smtp服务器链接
SMTP.set_debuglevel(level)：设置调试输出级别，值为1，2或True，发送调试消息到服务器
SMTP.send_message(msg,from_addr=None,to_addrs=None,mail_options=[],rcpt_options=[])：这是使用有email.message.Message对象
表示的消息进行调用的便捷方法使用sendmail()，参数的含义与sendmail()相同，只有msg是一个Message对象；如果from_addr是None或者
to_addrs是None，则send_message用从msg头部提取的地址填充那些参数，from设置为发件人自动，TO设置为to_addrs。
"""
from smtplib import SMTP

HOST = "mail.woniuxy.com"  # 定义smtp主机
#SUBJECT = "测试通过Python发送邮件"  # 定义邮件主题
SUBJECT = "This is mail from Python"  # 定义邮件主题
TO = "xulinlin@woniuxy.com"  # 定义邮件收件人
FROM = "student@woniuxy.com"  # 定义邮件发件人
PASSWD = "Student123"  # 定义邮件发送人密码
#text = "这是今天Agileone项目自动化测试报告，请查收！"  # 邮件内容,编码为ASCII范围内的字符或字节字符串，所以不能写中文
text = "This is Agileone Automation Report"
BODY = '\r\n'.join((  # 组合sendmail方法的邮件主体内容，各段以"\r\n"进行分离
    "From: %s" % FROM,
    "TO: %s" % TO,
    "subject: %s" % SUBJECT,
    "",
    text
))

if __name__ == '__main__':
    server = SMTP()  # 创建一个smtp对象
    server.connect(HOST, '25')  # 链接smtp主机
    server.login(FROM, PASSWD)  # 邮箱账号登陆
    server.sendmail(FROM, TO, BODY)  # 发送邮件
    server.quit()  # 端口smtp链接
