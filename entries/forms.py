import wtforms
from wtforms.validators import DataRequired

from models import Entry, Tag

class TagField(wtforms.StringField):
    def _value(self):
        """
        Convert the list of Tag instances into a comma-separated list of tag
        names.
        """
        if self.data:
            # Display tags as a comma-separated list.
            return ', '.join([tag.name for tag in self.data])
        return ''
        
    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        
        # Filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        
        # Query the database and retrieve any tags already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        
        # Determine which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        
        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name) for name in new_names]
        
        # Return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags
        
    def process_formdata(self, valuelist):
        """
        Accept the comma-separated tag list and convert it into a list of Tag
        instances.
        """
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

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
        
    tags = TagField(
        'Tags',
        description='Separate multiple tags with commas.'
    )
    
    def save_entry(self, entry):
        """
        Populate the entry passed in with the form data, regenerate
        the entry's slug based on the title.
        """
        self.populate_obj(entry)
        entry.generate_slug()
        return entry
        
class ImageForm(wtforms.Form):
    """
    Form to upload images.
    """
    file = wtforms.FileField('Image file')