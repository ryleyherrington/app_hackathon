"""Wrappers for authentication and authorization system.

Author: Dan Albert <dan@gingerhq.net>

Wrappers are used for authorization and authentication code in case we need to
introduce a different mechanism in the future.
"""
from google.appengine.api import users

from models import Group


def current_user():
    """Returns the User object for the signed in user or None."""
    return users.get_current_user()


def user_is_admin():
    """Returns True if the current user is an administrator."""
    return users.is_current_user_admin()


def logged_in():
    """Returns true if a user is currently logged in."""
    return current_user() is not None


def login_logout(request):
    """Generates text and a URL for a login/logout link.

    If a user is currently logged in, this returns a logout string and URL. If
    no user is logged in, this returns a login string and URL.

    Returns: a tuple of the form (text, URL)
    """
    if logged_in():
        url = users.create_logout_url(request.uri)
        text = 'Logout'
    else:
        url = users.create_login_url(request.uri)
        text = 'Login'

    return (text, url)


def user_from_email(email):
    """Returns the GAE user object associated with a given email address."""
    return users.User(email=email)


class User(object):
    """A wrapper for the GAE User class.

    TODO: We needed to add some custom methods to the GAE User class, and this
          was the simplest way to do that. Extending the User class would be
          cleaner, but that will require writing a custom datastore property
          type. Going forward, this should be done, but this works for now.
    """
    def __init__(self, user):
        self.gae_user = user

    def __eq__(self, other):
        if type(other) is users.User:
            return self.user_id == other.user_id()
        elif type(other) is User:
            return self.user_id == other.user_id
        else:
            return self == other

    @property
    def user_id(self):
        """Returns the user ID for the user."""
        return self.gae_user.user_id()

    @property
    def group(self):
        """The group the user belongs to, or None."""
        for group in Group.all():
            if self.gae_user in group.members:
                return group
        return None

    def in_group(self):
        """Returns True if the user is in a group, else returns False."""
        return self.group is not None

    def pending_join(self):
        """Returns True if the user is pending approval to join a group."""
        for group in Group.all():
            for user in group.pending_users:
                if user.user_id() == self.user_id:
                    return True
        return False

    def owns_a_group(self):
        """Returns True if the user owns his/her group, else returns False."""
        try:
            return self.group.owner == self.gae_user
        except AttributeError:
            return False
