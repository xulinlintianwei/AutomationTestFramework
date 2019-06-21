import smtplib
from email.utils import make_msgid,formatdate
from email.mime.text import MIMEText #html格式和文本格式邮件
from email.mime.multipart import MIMEMultipart #带多个部分的邮件
from email.mime.image import MIMEImage #带图片格式邮件
from email.mime.audio import MIMEAudio  #音频文件对象
from email.utils import formataddr   #分隔标题与地址
from email.header import Header   #设置标题字符集
from email import encoders  #编码器
from email.mime.application import MIMEApplication  #主要类型的MIME消息对象应用
from email.mime.base import MIMEBase

# 发件人地址，通过控制台创建的发件人地址
username = 'student@woniuxy.com'  # 定义邮件发件人
# 发件人密码，通过控制台创建的发件人密码
password = 'Student123'
# 自定义的回复地址
replyto = 'student@woniuxy.com'
# 收件人地址
rcptto = 'xulinlin@woniuxy.com'
HOST = "mail.woniuxy.com"  # 定义smtp主机

#构建信件标头结构

msg = MIMEMultipart('alternative')  #创建一个多部分的邮件对象
msg['Subject'] = Header('自定义信件主题', 'utf-8')
msg['From'] = formataddr(["学生",username])
msg['To'] = formataddr(['老师们',rcptto])
msg['Subject'] = "测试通过Python发送邮件"
msg['Reply-to'] = replyto
msg['Message-id'] = make_msgid() #Message-ID标头
msg['Date'] = formatdate()  #日期


#构建文本邮件内容
msg_text = MIMEText('自定义TEXT纯文本部分','plain','utf-8')
msg.attach(msg_text)
#读取文件创建邮件内容
with open('mailfile','rb') as fp:   #读取文件内容
    msg_text=MIMEText(fp.read(),'plain','utf-8')

#构建HTML格式的邮件内容
msg_html = MIMEText("<h1>HTML格式邮件</h1>","html","utf-8")
msg.attach(msg_html)

#构建HTML格式邮件带图片内容
html1 = "<div><img src='cid:imgid'></div>"
msg_html_img = MIMEText(html1,'html','utf-8')
msg.attach(msg_html_img)

with open("report.png","rb") as f:
    msg_img = MIMEImage(f.read())
msg_img.add_header('Content-ID','imgid') #扩展图片标题
msg.attach(msg_img)

#带附件的邮件MIMEApplication
filename = 'project.pdf'
with open(filename,'rb') as f:
    attachfile = MIMEApplication(f.read())
attachfile.add_header('Content-Disposition', 'attachment', filename=filename)
msg.attach(attachfile)

#带多个附件的邮件MIMEApplication
filenames = ['project.pdf','projectb.pdf']
for tmp in filenames:
    with open(tmp,'rb') as f:
        attachfiles = MIMEApplication(f.read())
        attachfiles.add_header('Content-Disposition', 'attachment', filename=tmp)
        msg.attach(attachfiles)

#带附件的邮件MIMEBase
filename1 = 'project.pdf'
attachfile_base = MIMEBase('application', 'octet-stream')  #创建基础对象指定类型
attachfile_base.set_payload(open(filename,'rb').read())  #设置我有效负载
attachfile_base.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', filename1) )
encoders.encode_base64(attachfile_base)
msg.attach(attachfile_base)

#创建音频文件
AUDIO_HTML = '''
    <p>this's audio file</p>
    <audio controls>
    <source src="cid:audioid" type="audio/mpeg">
    </audio>
'''
msg_test1 = MIMEText(AUDIO_HTML,'html','utf-8')
msg_audio = MIMEAudio(open('done.mp3','rb').read(),'plain')
msg_audio.add_header('Content-ID','audioid')
msg.attach(msg_test1)
msg.attach(msg_audio)

#收到邮件不能播放，有待解决！
if __name__ == '__main__':

    # 发送邮件
    try:
        client = smtplib.SMTP()
        #需要使用SSL，可以这样创建client
        #client = smtplib.SMTP_SSL()
        client.connect(HOST, "25")  # 通过 connect 方法连接 smtp 主机
        #开启DEBUG模式
        #client.set_debuglevel(1)
        client.login(username, password)
        client.sendmail(username, rcptto, msg.as_string())
        client.quit()
        print('email send success!')
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', e.message)
    except Exception as e:
        print('邮件发送异常, ', str(e))