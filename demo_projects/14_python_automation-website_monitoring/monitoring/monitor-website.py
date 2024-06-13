import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEBIAN_ROOT_PW = os.environ.get('DEBIAN_ROOT_PW')
LINODE_API_TOKEN = os.environ.get('LINODE_API_TOKEN')


def restart_server_and_container():
    # restart linode server
    print('Restarting Linode server')
    client = linode_api4.LinodeClient(LINODE_API_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 'REPLACE WITH NODE ID')
    nginx_server.reboot()

    while True:
        nginx_server = client.load(linode_api4.Instance, 'REPLACE WITH NODE ID')
        if nginx_server.status == 'running':
            time.sleep(5)  # wait for the server to fully boot up
            restart_container()
            break


def restart_container():
    print('Restarting the container of the application')
    # restart the docker container of the application
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # this will automatically add the hostname and new host key (so no need to type yes)
    pkey = paramiko.RSAKey.from_private_key_file("/home/kevinp/.ssh/devopscourse")
    ssh.connect(hostname='172.104.229.26', username='root', password=DEBIAN_ROOT_PW, pkey=pkey, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('docker start REPLACE_WITH_CONTAINER_ID')
    print(stdout.readlines())
    ssh.close()
    print('Container has been restarted!')


def send_notification(subject, body):
    print('Sending email notification')
    # send email
    # 'with' does the exception handling for us
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        print('Email has been sent!')


def monitor_application():
    try:
        response = requests.get('REPLACE WITH LINODE DOMAIN NAME')

        if response.status_code == 200:
            print('Website is up and running!')
        else:
            print('Website is down!')
            subject = 'Your website is down!'
            body = f'Make sure the server restarted and it is back up. Application returned status code: {response.status_code}'
            send_notification(subject, body)

            restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')

        subject = 'Your website is down!'
        body = 'Make sure the server restarted and it is back up. Application not accessible at all'
        send_notification(subject, body)

        restart_server_and_container()


schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()
