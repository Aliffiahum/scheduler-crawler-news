from apscheduler.schedulers.blocking import BlockingScheduler

from app.pipeline.pipeline_runner import PipelineRunner


scheduler = BlockingScheduler()


@scheduler.scheduled_job(
    "interval",
    minutes=30,
)
def run_pipeline():

    PipelineRunner().run()


if __name__ == "__main__":

    print("Scheduler started...")

    scheduler.start()