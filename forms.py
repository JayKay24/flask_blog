import wtforms
from wtforms import validators
from models import User

class LoginForm(wtforms.Form):
    email = wtforms.StringField("Email",
            validators=[validators.DataRequired()])
    
    password = wtforms.PasswordField("Password",
            validators=[validators.DataRequired()])
    
    remember_me = wtforms.BooleanField("Remember me?",
            default=True)
            
    # By default, full-email validation with wtforms is extremely difficult.
    # Override the forms validate method.
    def validate(self):
        """
        In the event the email is not found or the password does not match,
        display an error below the email field.
        """
        if not super(LoginForm, self).validate():
            return False
            
        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password")
            return False
        return True