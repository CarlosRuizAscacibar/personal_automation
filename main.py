#!/usr/bin/python

import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
[sys.path.append(path +'/'+o) 
    for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]

import zank
import notification
import bottle
import traceback
import evo
import fotocasa
import log
import exception_handler

'''
A basic bottle app skeleton
'''


app = application = bottle.Bottle()

@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./static')

@app.route('/')
def show_index():
    '''
    The front "index" page
    '''
    return 'Hello'

@app.route('/zank')
def check_zank():
    try:
        return zank.check_zank_loans()
    except:
        notification.send_notification("Exception in personal Automation",traceback.format_exc())
        return traceback.format_exc()

@app.route('/evo_weekly')
def evo_weekly(output, budget):
    try:
        if output == 'console':
            log._print(evo.weekly_report_text(budget))
        if output == 'email':
            notification.send_notification("EVO Weekly report",evo.weekly_report_html(budget))
    except:
        exception_handler._handle_exception("Exception in EVO weekly report")

@app.route('/fotocasa_periodic_scrap')
def fotocasa_periodic_scrap():
    try:
        fotocasa.periodic_scrap()
    except:
        exception_handler._handle_exception()
    
@app.route('/fotocasa_update_all')
def fotocasa_update_all():
    try:
        fotocasa.update_all()
    except:
        exception_handler._handle_exception()

class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    bottle.run(app=StripPathMiddleware(app),
        server='auto',
        host='0.0.0.0',
        port=8080)