from moduleframework import module_framework


class PythonTest(module_framework.AvocadoTest):
    PYTHON = 'python3'
    PY_VER = '3.6'
    PIP = 'pip3'
    SITE_PACKAGES_ARCH = '/usr/lib64/python{0}/site-packages'.format(PY_VER)
    SITE_PACKAGES = '/usr/lib/python{0}/site-packages'.format(PY_VER)
    LOCAL_SITE_PACKAGES = '/usr/local/lib/python{0}/site-packages'.format(
        PY_VER)
    LOCAL_SITE_PACKAGES_ARCH = \
        '/usr/local/lib64/python{0}/site-packages'.format(PY_VER)

    def pkg_install_sys(self, package, rpmbuild=False, silent=False):
        if silent:
            base_cmd = 'echo '' | sudo -S {0}{1} install {2}'
        else:
            base_cmd = 'sudo {0}{1} install {2}'

        env = 'RPM_BUILD_ROOT=/builddir/build/ ' if rpmbuild else ''

        self.run(base_cmd.format(env, self.PIP, package))
