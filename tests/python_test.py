from moduleframework import module_framework


class PythonAvocadoTest(module_framework.AvocadoTest):
    PYTHON = 'python3'
    PY_VER = '3.6'
    PIP = 'pip3'

    PREFIX = '/usr/'
    LOCAL_PREFIX = '/usr/local/'

    SITE_PACKAGES_ARCH = '{0}lib64/python{1}/site-packages'.format(
        PREFIX, PY_VER)
    SITE_PACKAGES = '{0}lib/python{1}/site-packages'.format(PREFIX, PY_VER)
    LOCAL_SITE_PACKAGES = '{0}lib/python{1}/site-packages'.format(
        LOCAL_PREFIX, PY_VER)
    LOCAL_SITE_PACKAGES_ARCH = \
        '{0}lib64/python{1}/site-packages'.format(LOCAL_PREFIX, PY_VER)

    VENV_ACTIVATE = 'source venv/bin/activate'

    def pkg_install_sys(self, package, rpmbuild=False):
        env = 'RPM_BUILD_ROOT=/builddir/build/ ' if rpmbuild else ''
        self.run('sudo {0}{1} install {2}'.format(env, self.PIP, package))

    def pkg_install_user(self, package):
        self.run('{0} install --user {1}'.format(self.PIP, package))

    def pkg_uninstall_sys(self, package, rpmbuild=False):
        env = 'RPM_BUILD_ROOT=/builddir/build/ ' if rpmbuild else ''
        self.run('sudo {0}{1} uninstall -y {2}'.format(env, self.PIP, package))

    def create_virtualenv(self, path, system_site=False):
        site_packages = ' --system-site-packages' if system_site else ''
        self.run('virtualenv-3 {0} -p /usr/bin/{1}{2}'.format(
            path, self.PYTHON, site_packages))

    def create_venv(self, path, system_site=False):
        site_packages = ' --system-site-packages' if system_site else ''
        self.run('{0} -m venv {1}{2}'.format(self.PYTHON, path, site_packages))

    def get_module_attr(self, module, attr='__file__', flag=''):
        return self.run("{0} {1} -c 'import {2}; print({2}.{3})'".format(
            self.PYTHON, flag, module, attr), shell=True).stdout
