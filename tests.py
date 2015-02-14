import unittest2 as unittest
import os
import tempfile
import shutil

from scripttest import TestFileEnvironment


class BaseTemplateTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

        # docs http://pythonpaste.org/scripttest/
        self.env = TestFileEnvironment(
            os.path.join(self.tempdir, 'test-output'),
            ignore_hidden=False,
        )

    def create_template(self):
        """Run mr.bob to create your template."""
        options = {
            'dir': os.path.join(os.path.dirname(__file__)),
            'template': self.template,
            'project': self.project,
            'answers_file': self.answers_file,
        }
        return self.env.run(
            '%(dir)s/bin/mrbob -O %(project)s --config '
            '%(dir)s/%(answers_file)s %(dir)s/bobtemplates/%(template)s'
            % options)


class PythonTemplateTest(BaseTemplateTest):
    """Tests for the `plone_addon` template."""
    template = ''
    project = ''
    answers_file = ''

    def test_python_project_template(self):
        """Test the `python_project` template.

        Generate a project from a template, test which files were created
        and run all tests in the generated package.
        """
        self.template = 'python_project'
        self.project = 'collective.foo'
        self.answers_file = 'test_answers.ini'
        result = self.create_template()
        self.assertItemsEqual(
            result.files_created.keys(),
            [
                self.project,
                self.project + '/.gitignore',
                self.project + '/.travis.yml',
                self.project + '/CHANGES.rst',
                self.project + '/CONTRIBUTORS.rst',
                self.project + '/MANIFEST.in',
                self.project + '/README.rst',
                self.project + '/bootstrap.py',
                self.project + '/buildout.cfg',
                self.project + '/docs',
                self.project + '/docs/LICENSE.GPL',
                self.project + '/docs/LICENSE.rst',
                self.project + '/setup.py',
                self.project + '/src',
                self.project + '/src/collective',
                self.project + '/src/collective/__init__.py',
                self.project + '/src/collective/foo',
                self.project + '/src/collective/foo/__init__.py',
                self.project + '/src/collective/foo/tests',
                self.project + '/src/collective/foo/tests/__init__.py',
                self.project + '/travis.cfg',
                self.project + '/.coveragerc',
            ]
        )

    def test_python_project_nested_template(self):
        """Test the `python_project_nested` template.

        Generate a project from a template, test which files were created
        and run all tests in the generated package.
        """
        self.template = 'python_project_nested'
        self.project = 'collective.foo.bar'
        self.answers_file = 'test_answers_nested.ini'
        self.maxDiff = None
        result = self.create_template()
        self.assertItemsEqual(
            result.files_created.keys(),
            [
                self.project,
                self.project + '/.gitignore',
                self.project + '/.travis.yml',
                self.project + '/CHANGES.rst',
                self.project + '/CONTRIBUTORS.rst',
                self.project + '/MANIFEST.in',
                self.project + '/README.rst',
                self.project + '/bootstrap.py',
                self.project + '/buildout.cfg',
                self.project + '/docs',
                self.project + '/docs/LICENSE.GPL',
                self.project + '/docs/LICENSE.rst',
                self.project + '/setup.py',
                self.project + '/src',
                self.project + '/src/collective',
                self.project + '/src/collective/__init__.py',
                self.project + '/src/collective/foo',
                self.project + '/src/collective/foo/__init__.py',
                self.project + '/src/collective/foo/bar',
                self.project + '/src/collective/foo/bar/__init__.py',
                self.project + '/src/collective/foo/bar/tests',
                self.project + '/src/collective/foo/bar/tests/__init__.py',
                self.project + '/travis.cfg',
                self.project + '/.coveragerc',
            ]
        )
