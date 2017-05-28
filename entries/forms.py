import wtforms
from wtforms.validators import DataRequired

from models import Entry

class EntryForm(wtforms.Form):
    """
    Form to enter blog entries.
    """
    title = wtforms.StringField(
        'Title', validators=[DataRequired()])
        
    body = wtforms.TextAreaField(
    'Body', validators=[DataRequired()])
    
    status = wtforms.SelectField(
        'Entry Status',
        choices=(
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')),
        # Force the value into an integer.
        coerce=int)
    
    def save_entry(self, entry):
        """
        Populate the entry passed in with the form data, regenerate
        the entry's slug based on the title.
        """
        self.populate_obj(entry)
        entry.generate_slug()
        return entry