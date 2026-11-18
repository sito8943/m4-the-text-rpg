from prefabs import validations

class ValidationManager:
    def __init__(self):
        self.rules = validations.rules()

    def validate(self, data, rules=None):
        """
        Validate the given data against the specified rules.
        :param data: A dictionary containing the data to validate.
        :param rules: A dictionary containing the validation rules. If None, use the default rules.
        :return: A dictionary containing any validation errors. If there are no errors, return an empty dictionary.
        """
        validation_rules = self.rules[rules]
        for _, rules in validation_rules.items():
            value = data
            for rule in rules:
                error = rule(value)
                if error:
                    return error
        return ""