import time

import schedule

from app.scheduler.pipeline import EditorialPipeline


class EditorialScheduler:

    def __init__(self):

        self.pipeline = EditorialPipeline()

    def job(self):

        print()

        print("=" * 70)
        print("START SCHEDULED JOB")
        print("=" * 70)

        self.pipeline.run()

        print()

    def start(self):

        schedule.every(30).minutes.do(self.job)

        print()

        print("Scheduler started...")

        print("Running every 30 minutes.")

        print()

        self.job()

        while True:

            schedule.run_pending()

            time.sleep(1)