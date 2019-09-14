import sys
sys.path.append('db/')
import requests
import pykeepass
import json
import db_zank
import traceback
try:

  # password is in a file inside computer and service
  vault_pass = open('pass.txt','r',encoding='utf-8').readline()
  vault = pykeepass.PyKeePass('vault.kdbx',password=vault_pass)

  # collect passwords from kdbx
  zank = [x for x in vault.entries if x.title == 'zank'][0]
  mailgun = [x for x in vault.entries if x.title == 'mailgun'][0]
  mailgun_key=mailgun.custom_properties['apikey']
  
  def notification(subject, text):
    requests.post(
        "https://api.mailgun.net/v3/sandbox251ead2c26cb4ebc912a952465022c6a.mailgun.org/messages",
        auth=("api", mailgun_key),
        data={"from": "Mailgun Sandbox <postmaster@sandbox251ead2c26cb4ebc912a952465022c6a.mailgun.org>",
          "to": "Carlos Ruiz <swsafetydance@gmail.com>",
          "subject": "Zank new loan",
          "text": text}
    )


  headers = {
      'authority': 'www.zank.com.es',
      'cache-control': 'max-age=0',
      'origin': 'https://www.zank.com.es',
      'upgrade-insecure-requests': '1',
      'content-type': 'application/x-www-form-urlencoded',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-user': '?1',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
      'sec-fetch-site': 'same-origin',
      'referer': 'https://www.zank.com.es/',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'es-ES,es;q=0.9',
      'cookie': '_ga=GA1.3.2060525521.1567941349; _gid=GA1.3.1510344404.1567941349; __utma=34198954.2060525521.1567941349.1567941350.1567941350.1; __utmc=34198954; __utmz=34198954.1567941350.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; _gat=1; PHPSESSID=gub6jbfh5uldtl8vh8hkul48vj; __utmb=34198954.10.9.1567941567563; _gali=_submit; __utmli=_submit',
  }

  data = {
    '_username': zank.username,
    '_password': zank.password
  }

  response_login = requests.post('https://www.zank.com.es/login_check', headers=headers, data=data)



  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Referer': 'https://www.zank.com.es/login',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'Cache-Control': 'max-age=0',
      'TE': 'Trailers',
  }

  response = requests.get('https://www.zank.com.es/investor/listLoans', headers=headers, cookies=response_login.cookies)
  data = response.text
  dic_answer_loans = json.loads(data)
  added_loans = []
  for loan in dic_answer_loans['data']:
    new_loan_id = str(loan['CreditoId'])
    stored_load = db_zank.get_lend_external_id(new_loan_id)
    if stored_load == None:
      added_loans.append(new_loan_id)
      db_zank.create_lend(new_loan_id)

  if len(added_loans) > 0:
    notification("Personal Automation: "+ str(len(added_loans)) +" New loans", "There are " + str(len(added_loans)) + " new lends")
  else:
    print('No new lends')
except:
  notification("Exception in personal Automation",traceback.format_exc())






