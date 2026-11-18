from prefabs import validations

class ValidationManager:
    def __init__(self):
        self.rules = validations.rules()

    def validate(self, data, rules):
        """
        Validate the given data against the specified rules.
        :param data: The value to validate.
        :param rules: The name of the rule set to use (e.g. "name").
        :return: The first error message found, or None if the data is valid.
        """
        for checks in self.rules[rules].values():
            for check in checks:
                error = check(data)
                if error:
                    return error
        return None
