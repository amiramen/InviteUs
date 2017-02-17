from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite', convert_unicode=True)
# engine = create_engine('mysql://root:toor@localhost/invite_us_php')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    
	import models
	Base.metadata.create_all(bind=engine)
	
if __name__ == "__main__":
	import sys
	if sys.argv.count > 1 and sys.argv[1] == "init_db":
		print "init_db...",
		init_db();
		print "Done"

