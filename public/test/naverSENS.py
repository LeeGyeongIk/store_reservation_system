import time
import requests
import hashlib
import hmac
import base64

def send_sms(sms_from, sms_to, subject, message):
  def make_signature(access_key, secret_key, method, uri, timestmap):
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

  #  URL
  url = 'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:283399960131:store_reservation_system/messages'
  # access key
  access_key = 'cIwMSA071UAG5IhJ3VGG'
  # secret key
  secret_key = 'vGPparPQbl5O4hStXb9ProhOWE7XdhFsuo3mQz1k'
  # uri
  uri = '/sms/v2/services/ncp:sms:kr:283399960131:store_reservation_system/messages'
  timestamp = str(int(time.time() * 1000))

  body = {
    "type":"LMS",
    "contentType":"COMM",
    "countryCode":"82",
    "from":sms_from,
    "content": message,
    "messages":[
        {
            "to": sms_to,
            "subject": subject,
            "content": message
        }
    ]
  }

  key = make_signature(access_key, secret_key, 'POST', uri, timestamp)
  headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-ncp-apigw-timestamp': timestamp,
    'x-ncp-iam-access-key': access_key,
    'x-ncp-apigw-signature-v2': key
  }


  res = requests.post(url, json=body, headers=headers)
  print(res.json())
  return res.json()

send_sms("01037225398","01051683224","subject","오늘안에 5000만원 입금하세요")