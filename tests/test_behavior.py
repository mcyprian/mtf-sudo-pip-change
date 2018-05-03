#!/usr/bin/python3

from avocado import main
from python_test import PythonAvocadoTest


class SimpleTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_print(self):
        self.start()
        self.assertIn('It works!',
                      self.run("python3 -c \"print('It works!')\"", shell=True)
                      .stdout)

    def test_prefix(self):
        self.start()
        self.assertEquals('/usr\n',
                          self.run("python3 -c 'import sys; print(sys.prefix)'",
                                   shell=True)
                          .stdout)

    def test_site_packages(self):
        self.start()
        self.assertEquals(
            '{0}\n'.format(self.LOCAL_SITE_PACKAGES_ARCH),
            self.run(
                "python3 -c 'import site; print(site.getsitepackages()[0])'",
                shell=True).stdout)

    def test_path(self):
        self.start()
        self.pkg_install_sys('jinja2')
        self.assertEquals(
            '{0}\n'.format(self.LOCAL_SITE_PACKAGES_ARCH),
            self.run(
                "python3 -c 'import sys; print(sys.path[4])'",
                shell=True).stdout)

        self.assertEquals(
            '{0}\n'.format(self.LOCAL_SITE_PACKAGES),
            self.run(
                "python3 -c 'import sys; print(sys.path[5])'",
                shell=True).stdout)

        self.assertEquals(
            '{0}\n'.format(self.SITE_PACKAGES_ARCH),
            self.run(
                "python3 -c 'import sys; print(sys.path[6])'",
                shell=True).stdout)


class ImportTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_std_lib(self):
        self.start()
        self.assertNotIn('Traceback (most recent call last):',
                         self.run("python3 -c 'import sys, os, asyncio'",
                                  shell=True).stdout)


class InstallLocationTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_user_environ(self):
        self.start()
        self.pkg_install_sys('jinja2')
        self.pkg_install_sys('simplejson')
        self.assertIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertIn(
            self.LOCAL_SITE_PACKAGES,
            self.run(
                "python3 -c 'import simplejson; print(simplejson.__file__)'",
                shell=True).stdout)

    def test_rpm_build(self):
        self.start()
        self.pkg_install_sys('jinja2', rpmbuild=True)
        self.pkg_install_sys('simplejson', rpmbuild=True)
        self.assertIn(
            self.SITE_PACKAGES_ARCH,
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertIn(
            self.SITE_PACKAGES,
            self.run(
                "python3 -c 'import simplejson; print(simplejson.__file__)'",
                shell=True).stdout)


class IsolationTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_dash_i(self):
        self.start()
        self.pkg_install_sys('jinja2')
        self.assertNotIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.get_module_attr('sys', 'path', flag='-I'))

    def test_dash_s(self):
        self.start()
        self.pkg_install_sys('jinja2')
        self.assertNotIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.get_module_attr('sys', 'path', flag='-s'))


class NonSystemInstallationTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_user(self):
        self.start()
        self.run('pip3 install --user jinja2')
        self.assertIn(
            '/home/testuser/.local/lib/python3.6/site-packages',
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)

    def test_virtualenv(self):
        self.start()
        self.create_virtualenv('/home/testuser/venv')
        self.run("source venv/bin/activate && pip3 install jinja2")
        self.assertIn(
            '/home/testuser/venv/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import jinja2; "
                "print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertNotIn(
            '{0}\n'.format(self.LOCAL_SITE_PACKAGES),
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)

    def test_virtualenv_system_site(self):
        self.start()
        self.create_virtualenv('/home/testuser/venv', system_site=True)
        self.run("sudo pip3 install jinja2 && source venv/bin/activate")
        self.assertIn(
            '/home/testuser/venv/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            self.LOCAL_SITE_PACKAGES,
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            self.SITE_PACKAGES,
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)

    def test_venv(self):
        self.start()
        self.run('python3 -m venv /home/testuser/venv')
        self.run("source venv/bin/activate && pip3 install jinja2")
        self.assertIn(
            '/home/testuser/venv/lib64/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import jinja2; "
                "print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertNotIn(
            self.LOCAL_SITE_PACKAGES,
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)

    def test_venv_system_site(self):
        self.start()
        self.run('python3 -m venv /home/testuser/venv --system-site-packages')
        self.run("sudo pip3 install jinja2 && source venv/bin/activate")
        self.assertIn(
            '/home/testuser/venv/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            self.LOCAL_SITE_PACKAGES,
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            self.SITE_PACKAGES,
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)


class EmbededPythonBinaryTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_local_import(self):
        self.start()
        self.pkg_install_sys('jinja2')
        self.run('sudo cp /usr/bin/python3 /usr/local/bin/embeded-py-bin')
        self.assertIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.run(
                "embeded-py-bin -c 'import sys; print(sys.path)'",
                shell=True).stdout)
        self.assertNotIn('Traceback (most recent call last):',
                         self.run(
                             "embeded-py-bin -c 'import jinja2'",
                             shell=True).stdout)


class PipUninstallTest(PythonAvocadoTest):
    """
    :avocado: enable
    """

    def test_uninstall_ok(self):
        self.start()
        self.pkg_install_sys('jinja2')
        self.assertIn(
            self.LOCAL_SITE_PACKAGES_ARCH,
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)
        self.pkg_uninstall_sys('jinja2')
        self.assertNotIn("jinja2'",
                         self.run("{0} freeze".format(self.PIP),
                                  shell=True).stdout)

    def test_uninstall_not_ok(self):
        self.start()
        self.pkg_install_sys('jinja2', rpmbuild=True)
        self.assertIn(
            self.SITE_PACKAGES_ARCH,
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)
        self.pkg_uninstall_sys('jinja2')
        self.assertIn("jinja2'", self.run("{0} freeze".format(self.PIP),
                                          shell=True).stdout)

    def test_uninstall_setuptools(self):
        self.start()
        self.pkg_install_sys('setuptools')
        self.pkg_uninstall_sys('setuptools')
        self.run(
            "{0} -Es -c 'import setuptools; print(setuptools.__file__)'".format(
                self.PYTHON), shell=True)


if __name__ == '__main__':
    main()
