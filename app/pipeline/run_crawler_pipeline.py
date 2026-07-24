from app.pipeline.pipeline_runner import PipelineRunner

runner = PipelineRunner()

runner.collector()
runner.preprocessing()
runner.sentiment()