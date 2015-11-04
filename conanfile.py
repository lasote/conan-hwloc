from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake


class HWLOCConan(ConanFile):
    name = "hwloc"
    version = "1.11.1"
    ZIP_FOLDER_NAME = "hwloc-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    url="http://github.com/lasote/conan-zlib"
    
    def system_requirements(self):
        if self.settings.os == "Linux":
            self.run("sudo apt-get install libudev1 libudev1:i386")
            self.run("sudo apt-get install libudev-dev libudev-dev:i386")
            self.run("sudo apt-get install libxml2-dev libxml2-dev:i386")

    def conan_info(self):
        # We don't want to change the package for each compiler version but
        # we need the setting to compile with cmake
        self.info.settings.compiler.version = "any"

    def source(self):
        zip_name = "hwloc.tar.gz"
        major = ".".join(self.version.split(".")[0:2])
        download("http://www.open-mpi.org/software/hwloc/v%s/downloads/hwloc-%s.tar.gz" % (major, self.version), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            shared_options = "--enable-shared" if self.options.shared else "--enable-static"
            arch = "-m32 " if self.settings.arch == "x86" else ""
            
            if self.settings.os == "Macos":
                old_str = 'install_name \$rpath/\$soname'
                new_str = 'install_name \$soname'
                replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
            
            self.run("cd %s && CFLAGS='%s -mstackrealign -fPIC -O3' ./configure %s" % (self.ZIP_FOLDER_NAME, arch, shared_options))
            self.run("cd %s && make" % self.ZIP_FOLDER_NAME)
        else:
#             cmake = CMake(self.settings)
#             if self.settings.os == "Windows":
#                 self.run("IF not exist _build mkdir _build")
#             else:
#                 self.run("mkdir _build")
#             cd_build = "cd _build"
#             self.output.warn('%s && cmake .. %s' % (cd_build, cmake.command_line))
#             self.run('%s && cmake .. %s' % (cd_build, cmake.command_line))
#             self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
#             self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
            pass

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        self.copy(pattern="*.h", dst="include", src="%s/include" % (self.ZIP_FOLDER_NAME), keep_path=True)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                    self.copy(pattern="*.so.*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['hwloc']
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["udev", "xml2"])


def replace_in_file(file_path, search, replace):
    with open(file_path, 'r') as content_file:
        content = content_file.read()
        content = content.replace(search, replace)
    with open(file_path, 'wb') as handle:
        handle.write(content)
