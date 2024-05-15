import logging
from datetime import datetime


logger = logging.getLogger(__name__)

def log_user_activity(user, action, message):
    """
    Log user activity.

    Args:
    - user: The user performing the action.
    - action: A string representing the action performed by the user.
    - message: Additional information or message related to the action.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{now} | User: {user.full_name} | Action: {action} | Message: {message}"
    logger.info(log_message)
