from flask_wtf import FlaskForm
from wtforms import FieldList, StringField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


class CreateJobForm(FlaskForm):
    title = StringField("title", [DataRequired(), Length(max=50, min=5)])
    seniority = StringField("seniority", [DataRequired()])
    mandatory_knowledge = FieldList(StringField("mandatory_knowledge", [Optional()]))
    optional_knowledge = FieldList(StringField("optional_knowledge", [Optional()]))

    def validate_on_submit(self, extra_validators=None):
        super().validate_on_submit(extra_validators)
        # Check if any additional fields were sent
        for field in self.data:
            if field not in self._fields:
                raise ValidationError("This field is not allowed.")
