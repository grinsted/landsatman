from config import huey
import time
import download_helper


@huey.task()
def fetch(sceneid):
    print 'fetching: %s' % sceneid
    return download_helper.download(sceneid)
    