from neksflis.celery import app


@app.task
def deactivate_unsubscribed_users():
    # deactivate users that unsubscribed long ago.
    pass
