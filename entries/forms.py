import wtforms

from models import Entry

class EntryForm(wtforms.Form):
    """
    Form to enter blog entries.
    """
    title = wtforms.StringField('Title')
    body = wtforms.TextAreaField('Body')
    status = wtforms.SelectField(
        'Entry Status',
        choices=(
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')),
        # Force the value into an integer.
        coerce=int)