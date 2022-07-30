import redis


def setupdb(url, password, db, port):
    db = redis.StrictRedis(
        host=url,
        password=password,
        port=port,
        db=db,
        decode_responses=True
    )
    return(db)
