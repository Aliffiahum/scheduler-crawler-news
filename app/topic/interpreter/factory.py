from app.topic.interpreter.rule_based import RuleBasedInterpreter


class TopicInterpreterFactory:

    @staticmethod
    def create():

        return RuleBasedInterpreter()