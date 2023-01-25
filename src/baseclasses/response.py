from pydantic.error_wrappers import ValidationError


class Response:

    def __init__(self, response):
        self.response = response
        self.json_data = response.json()
        self.response_status = response.status_code
        self.parsed_object = None

    def validate(self, schema):
        try:
            if isinstance(self.json_data.get("data"), list):
                for item in self.json_data["data"]:
                    parsed_object = schema.parse_obj(item)
                    self.parsed_object = parsed_object
            else:
                schema.parse_obj(self.json_data)
        except ValidationError:
            raise AssertionError("Could not map received object to pydantic schema")

    def assert_status_code(self, status_code: int):
        if isinstance(status_code, list):
            assert self.response_status in status_code, self
        else:
            assert self.response_status == status_code, self
        return self

    def get_parsed_object(self):
        return self.parsed_object

    def __str__(self):
        return \
            f"\nStatus code: {self.response_status} \n" \
            f"Requested url: {self.response.url} \n" \
            f"Response body: {self.json_data}"
