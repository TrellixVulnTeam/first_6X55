import os
import click
import sys
from app import create_app, db
from app.models import User, Role, Permissions
from flask_migrate import Migrate
from flask_migrate import upgrade





os.environ['FLASK_COVERAGE'] = '1'
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permissions=Permissions)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run test under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable]+sys.argv)
    import unittest
    tests = unittest.TestLoader().loadTestsFromNames('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage summary')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s//index.html' % covdir)
        COV.erase()

@app.cli.command()
@click.option('--lengh', default=25,
              help='Number of function to include in the profiler report')
@click.option('--profile-dr', default=None,
              help='Directory where profiler data ar saved')
def profile(length, profile_dir):
    """Start the application under the code profile"""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run(debug=False)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

    # ensure all users are following themselves
    User.add_self_follows()
