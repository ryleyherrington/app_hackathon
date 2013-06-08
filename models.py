"""Models used by the app-hackathon application.

Author: Dan Albert <dan@gingerhq.net>
"""
from google.appengine.ext import db
from google.appengine.api import users


class Idea(db.Model):
    """A project idea."""
    name = db.StringProperty("Title of the project if the idea is approved")
    author = db.UserProperty("User that had the idea, or null if anonymous")
    description = db.TextProperty("Long description of the project")
    post_time = db.DateTimeProperty("Post time", auto_now_add=True)


class Project(db.Model):
    """A project which represents and idea that was approved by a moderator.

    Discussion:
        Should this model be combined with the Idea model? The idea remains the
        same throughout the process.

        Why do we even have a voting process? Why not let developers choose
        from the list of approved ideas?
    """
    name = db.StringProperty("Project title")
    author = db.UserProperty("User that had the idea, or null if anonymous")
    description = db.TextProperty("Long description of the project")
    post_time = db.DateTimeProperty("Idea submission time", auto_now_add=True)
    votes = db.ListProperty(users.User)
    # implicit member "groups" from the Group model

    def has_voted(self, user):
        """Returns true if the given user has voted for this project."""
        return user in self.votes

    def vote(self, user):
        """Adds the user's vote to this project."""
        if not self.has_voted(user):
            self.votes.append(user)
        # TODO: else should probably bitch and moan, but our error handling
        #       isn't so great right now

    def remove_vote(self, user):
        """Removes the user's vote from this project."""
        self.votes.remove(user)


class Group(db.Model):
    """A group of people that are working together on a project."""
    name = db.StringProperty("Name to identify the group")
    public = db.BooleanProperty("True if anyone may join the group")
    owner = db.UserProperty("The owner of this group")
    project = db.ReferenceProperty(Project, collection_name='groups')
    members = db.ListProperty(users.User)
    pending_users = db.ListProperty(users.User)
    # implicit member "submissions" from the submission model

    def __eq__(self, other):
        # TODO: this may not be necessary. it is unclear whether keys are
        #       unique throughout the datastore or just for each kind
        return other.__class__ == self.__class__ and self.key() == other.key()

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def exists(cls, name):
        """Returns True if a group by the given name already exists."""
        return Group.all().filter('name =', name).count() > 0


class Submission(db.Model):
    """A group's submission for their project.

    Submissions are hosted externally, and groups are allowed to post links to
    their submissions to our site.
    """
    text = db.StringProperty("Link text")
    url = db.LinkProperty("Link to submission")
    weight = db.IntegerProperty("Display order weight", default=0)
    group = db.ReferenceProperty(Group, collection_name='submissions')

    def to_a(self):
        """Returns the HTML anchor tag that represents this submission."""
        return '<a href="%s">%s</a>' % (self.url, self.text)
