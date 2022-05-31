import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr,formataddr

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1627184210@qq.com"  # 用户名
mail_pass = "qzxeefeczvrdedcd"  # 口令

sender = '1627184210@qq.com'
receivers = ['xuchenxi12138@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("数据库原理示范教学平台@qq.com",'utf-8')
message['To'] = Header("测试")
message['Subject'] = Header('Python SMTP 邮件测试12', 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(mail_user, receivers, message.as_string())
    smtpObj.quit()
    print("邮件发送成功")

except smtplib.SMTPException:
    print("Error: 无法发送邮件")
