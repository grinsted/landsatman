from huey import Huey
from huey.backends.sqlite_backend import SqliteQueue, SqliteDataStore

queue = SqliteQueue("queue", "db/queue.db")
result_store = SqliteDataStore("results", "db/results.db")

huey = Huey(queue, result_store=result_store)

settings={
'gsurl': 'gs://earthengine-public/landsat',
'targetfolder': 'landsatarchive'
}


