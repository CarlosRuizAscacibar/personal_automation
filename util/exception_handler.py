import notification
import log
import os
import traceback

def _handle_exception(msg="Exception in personal Automation"):
    """
        Handles notification by looking at environment variable PA_EXCEPTIONS
        to decide the notification output channel.

        msg is the message of the exception.
    """
    output = os.environ.get('PA_EXCEPTIONS','console')
    if output == 'console':
        log._print(traceback.format_exc())
    if output == 'email':
        notification.send_notification(msg, traceback.format_exc())