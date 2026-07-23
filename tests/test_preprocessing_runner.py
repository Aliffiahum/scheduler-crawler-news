from app.database.connection import SessionLocal

from app.preprocessing.preprocessing_runner import PreprocessingRunner


db = SessionLocal()

runner = PreprocessingRunner(db)

runner.run()

db.close()