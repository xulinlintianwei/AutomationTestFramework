"""
邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。

email.mime.multipart.MIMEMultipart（_subtype='mixed'，boundary= None，_subparts = None，*，policy = compat32，** _ params )：
作用是生成包含多个部分的邮件体的 MIME 对象，参数 _subtype 指定要添加到"Content-type:multipart/subtype" 报头的可选的三种子类型
，分别为 mixed、related、alternative，默认值为 mixed。定义 mixed实现构建一个带附件的邮件体；定义related 实现构建内嵌资源的邮
件体；定义alternative 则实现构建纯文本与超文本共存的邮件体；_subparts是有效负载的一系类初始部分，可以使用attach()方法将子部件
附加到消息中。

email.mime.text.MIMEText (_text[, _subtype[, _charset]])：
MIMENonMultipart中的一个子类，创建包含文本数据的邮件体，_text 是包含消息负载的字符串，_subtype 指定文本类型，支持 plain（默认值）
或 html类型的字符串。_charset设置字符集，参数接受一个charset实例。

参考网络文章：https://www.cnblogs.com/zhangxinqi/p/9113859.html
通过邮件传输简单的文本已经无法满足我们的需求，比如我们时常会定制业务质量报表，在邮件主体中会包含 HTML、图像、声音以及附件格式等，
MIME（Multipurpose Internet Mail Extensions，多用途互联网邮件扩展）作为一种新的扩展邮件格式很好地补充了这一点，
更多MIME 知识见 https://docs.python.org/3/library/email.html。
"""
import re
import smtplib
# 导入生成包含多个部分的邮件体的 MIME 对象
from email.mime.multipart import MIMEMultipart
# 创建包含文本数据的邮件体
from email.mime.text import MIMEText
# 导入 socket相关典型异常类
from socket import gaierror, error
# 导入之前封装好的处理日志类对象
from utils.log import logger
# 导入报告存放目录，发送邮件时需要用到报告的目录
from utils.config import REPORT_PATH


class Email(object):
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = title # 邮件标题，必填。
        self.message = message # 邮件正文，非必填。
        self.files = path # 附件路径，可传入list（多附件）或str（单个附件），非必填。

        # 定义related 实现构建内嵌资源的邮件体；
        self.msg = MIMEMultipart('related')

        self.server = server       # smtp服务器，必填。
        self.sender = sender       # 发件人，必填。
        self.receiver = receiver   # 收件人，多收件人用“；”隔开，必填。
        self.password = password   # 发件人密码，必填。

    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        # 创建包含文本数据的邮件体，_text 是包含消息负载的字符串，_subtype 指定文本类型，支持 plain（默认值）
        # _charset设置字符集，参数接受一个charset实例。
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        # 调试日志
        logger.debug('附件内容为{}'.format(att))
        """
        Content-Type，内容类型，一般是指网页中存在的Content-Type，用于定义网络文件的类型和网页的编码，决定浏览器
        将以什么形式、什么编码读取这个文件，这就是经常看到一些Asp网页点击的结果却是下载到的一个文件或一张图片的原因。
        参考：https://www.runoob.com/http/http-content-type.html
       """
        att["Content-Type"] = 'application/octet-stream'  # .*（ 二进制流，不知道下载文件类型）
        file_name = re.split(r'[\\|/]', att_file)
        """
        Content-disposition 是 MIME 协议的扩展，MIME 协议指示 MIME 用户代理如何显示附加的文件。
        Content-disposition 其实可以控制用户请求所得的内容存为一个文件的时候提供一个默认的文件名，文件直接在浏览器上
        显示或者在访问时弹出文件下载对话框。
        格式说明： content-disposition = "Content-Disposition" ":" disposition-type *( ";" disposition-parm ) 　
        字段说明：Content-Disposition为属性名disposition-type是以什么方式下载，如attachment为以附件方式下载
        disposition-parm为默认保存时的文件名服务端向客户端游览器发送文件时，如果是浏览器支持的文件类型，一般会默认
        使用浏览器打开，比如txt、jpg等，会直接在浏览器中显示，如果需要提示用户保存，就要利用Content-Disposition
        进行一下处理，关键在于一定要加上attachment：
       """
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        """具体发送邮件的函数"""
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP(self.server)  # 连接sever
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))


if __name__ == '__main__':
    print(REPORT_PATH)
    report = REPORT_PATH + '\\report.html'
    e = Email(title='Agileone项目测试报告',
              message='这是今天Agileone项目自动化测试报告，请查收！',
              receiver='xulinlin@woniuxy.com',
              server='mail.woniuxy.com',
              sender='student@woniuxy.com',
              password='Student123',
              path=report
              )
    e.send()