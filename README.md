The Development Environment
===========================

The project is now purely Google App Engine, which greatly simplifies the
development, staging and deployment of the website.

Start the development server using

    $ dev_appserver.py app-hackathon/

Then navigate to [http://127.0.0.1:8080/](http://127.0.0.1:8080/) and begin
testing the site.

Note: this needs to be run from the directory above the project.

Staging
=======

Once you have tested your changes locally, you can push them to the staging
server for a final test (or to share with other develpers) before pushing them
to the production site. To do this, change the application name in `app.yaml`
from app-hackathon to dev-app-hackathon. Now upload the application to Google
App Engine as usual.

Deployment
==========

Final deployment should be simple. Ensure that the application name in
`app.yaml` is app-hackathon, and run

    $ appcfg.py update app-hackathon/

Note: this needs to be run from the directory above the project.

Guidelines and Style
====================
* Make sure your HTML is valid and well indented. It is really difficult to
  figure out what the tag hierarchy is when the HTML is malformed, poorly
  indented, and written by someone else.
* Try to keep your lines limited to 80 characters. I'm often working from a
  terminal, and lines reaching into the hundreds of characters in length are
  very unwieldy.
* Avoid using memcaches. Premature optimization only makes development more
  difficult. If we see some parts of the site that would benefit from their use,
  file a bug and I'll take care of it.
* Let me (Dan) know before you make a database change. It's usually simpler to
  write it myself than it is to fix a bad implementation.
* Make sure your resources are in the right place. HTML templates go in
  `/templates`. Stylesheets, images and scripts go in `/static`.
* [Python style guide](http://www.python.org/dev/peps/pep-0008/)