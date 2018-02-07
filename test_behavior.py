#!/usr/bin/python3

from avocado import main
from moduleframework import module_framework


class SimpleTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testPrint(self):
        self.start()
        self.assertIn('It works!',
                      self.run("python3 -c \"print('It works!')\"", shell=True)
                      .stdout)

    def testPrefix(self):
        self.start()
        self.assertEquals('/usr\n',
                          self.run("python3 -c 'import sys; print(sys.prefix)'",
                                   shell=True)
                          .stdout)

    def testSitePackages(self):
        self.start()
        self.assertEquals(
            '/usr/local/lib64/python3.6/site-packages\n',
            self.run(
                "python3 -c 'import site; print(site.getsitepackages()[0])'",
                shell=True).stdout)

    def testPath(self):
        self.start()
        self.run('sudo pip3 install jinja2')
        self.assertEquals(
            '/usr/local/lib64/python3.6/site-packages\n',
            self.run(
                "python3 -c 'import sys; print(sys.path[4])'",
                shell=True).stdout)

        self.assertEquals(
            '/usr/local/lib/python3.6/site-packages\n',
            self.run(
                "python3 -c 'import sys; print(sys.path[5])'",
                shell=True).stdout)

        self.assertEquals(
            '/usr/lib64/python3.6/site-packages\n',
            self.run(
                "python3 -c 'import sys; print(sys.path[6])'",
                shell=True).stdout)


class ImportTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testStdLib(self):
        self.start()
        self.assertNotIn('Traceback (most recent call last):',
                         self.run("python3 -c 'import sys, os, asyncio'",
                                  shell=True).stdout)


class InstallLocationTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testUserEnviron(self):
        self.start()
        self.run("sudo pip3 install jinja2")
        self.run("sudo pip3 install simplejson")
        self.assertIn(
            '/usr/local/lib64/python3.6/site-packages',
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/local/lib/python3.6/site-packages',
            self.run(
                "python3 -c 'import simplejson; print(simplejson.__file__)'",
                shell=True).stdout)

    def testRPMBuild(self):
        self.start()
        self.run('sudo RPM_BUILD_ROOT=/builddir/build/ pip3 install jinja2')
        self.run(
            'sudo RPM_BUILD_ROOT=/builddir/build/ pip3 install simplejson')
        self.assertIn(
            '/usr/lib64/python3.6/site-packages',
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/lib/python3.6/site-packages',
            self.run(
                "python3 -c 'import simplejson; print(simplejson.__file__)'",
                shell=True).stdout)


class IsolationTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testDashI(self):
        self.start()
        self.run("echo '' | sudo -S pip3 install jinja2")
        self.assertNotIn(
            '/usr/local/lib64/python3.6/site-packages',
            self.run(
                "python3 -I -c 'import sys; print(sys.path)'",
                shell=True).stdout)

    def testDashS(self):
        self.start()
        self.run("echo '' | sudo -S pip3 install jinja2")
        self.assertNotIn(
            '/usr/local/lib64/python3.6/site-packages',
            self.run(
                "python3 -s -c 'import sys; print(sys.path)'",
                shell=True).stdout)


class NonSystemInstallationTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testUser(self):
        self.start()
        self.run('pip3 install --user jinja2')
        self.assertIn(
            '/home/testuser/.local/lib/python3.6/site-packages',
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)

    def testVirtualenv(self):
        self.start()
        self.run('virtualenv-3 /home/testuser/venv -p /usr/bin/python3')
        self.run("source venv/bin/activate && pip3 install jinja2")
        self.assertIn(
            '/home/testuser/venv/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import jinja2; "
                "print(jinja2.__file__)'",
                shell=True).stdout)
        self.assertNotIn(
            '/usr/local/lib/python3.6/site-packages\n',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)

    def testVirtualenvSystemSite(self):
        self.start()
        self.run('virtualenv-3 /home/testuser/venv -p /usr/bin/python3 '
                 '--system-site-packages')
        self.run("sudo pip3 install jinja2 && source venv/bin/activate")
        self.assertIn(
            '/home/testuser/venv/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/local/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/local/lib64/python3.6/site-packages',
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)

    def testVenv(self):
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
            '/usr/local/lib/python3.6/site-packages\n',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)

    def testVenvSystemSite(self):
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
            '/usr/local/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/lib/python3.6/site-packages',
            self.run(
                "source venv/bin/activate && python3 -c 'import sys; "
                "print(sys.path)'",
                shell=True).stdout)
        self.assertIn(
            '/usr/local/lib64/python3.6/site-packages',
            self.run(
                "python3 -c 'import jinja2; print(jinja2.__file__)'",
                shell=True).stdout)


class EmbededPythonBinaryTest(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testLocalImport(self):
        self.start()
        self.run('sudo pip3 install jinja2')
        self.run('sudo cp /usr/bin/python3 /usr/local/bin/embeded-py-bin')
        self.assertIn(
            '/usr/local/lib64/python3.6/site-packages',
            self.run(
                "embeded-py-bin -c 'import sys; print(sys.path)'",
                shell=True).stdout)
        self.assertNotIn('Traceback (most recent call last):',
                         self.run(
                             "embeded-py-bin -c 'import jinja2'",
                             shell=True).stdout)


if __name__ == '__main__':
    main()
