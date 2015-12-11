from conans import ConanFile
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake


class HWLOCConan(ConanFile):
    name = "hwloc"
    version = "1.11.1"
    ZIP_FOLDER_NAME = "hwloc-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindHwloc.cmake"]
    url="http://github.com/lasote/conan-hwloc"
    
    def system_requirements(self):
        self.global_system_requirements=True
        if self.settings.os == "Linux":
            self.output.warn("'libudev' library is required in your computer. Enter sudo password if required...")
            self.run("sudo apt-get install libudev0 libudev0:i386 || true ")
            self.run("sudo apt-get install libudev1 libudev1:i386 || true ")
            self.run("sudo apt-get install libudev-dev libudev-dev:i386 || true ")
            self.run("sudo apt-get install libxml2-dev libxml2-dev:i386 || true ")

    def conan_info(self):
        # We don't want to change the package for each compiler version but
        # we need the setting to compile with cmake
        # self.info.settings.compiler.version = "any"
        if self.settings.os == "Windows":
            self.info.settings.build_type = "Release"

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
        elif self.settings.os == "Windows":
            runtimes = {"MD": "MultiThreadedDLL",
                        "MDd": "MultiThreadedDebugDLL",
                        "MT": "MultiThreaded",
                        "MTd": "MultiThreadedDebug"}
            runtime = runtimes[str(self.settings.compiler.runtime)]
            file_path = "%s/contrib/windows/libhwloc.vcxproj" % self.ZIP_FOLDER_NAME
            # Adjust runtime in project solution
            replace_in_file(file_path, "MultiThreadedDLL", runtime)
            
            platform, configuration = self.visual_platform_and_config()
            msbuild = 'Msbuild.exe hwloc.sln /m /t:libhwloc /p:Configuration=%s;Platform="%s"' % (configuration, platform)
            self.output.info(msbuild)
            self.run("cd %s/contrib/windows/ &&  %s" % (self.ZIP_FOLDER_NAME, msbuild))

    def visual_platform_and_config(self):
        platform = "Win32" if self.settings.arch == "x86" else "x64"
        configuration = "Release" if self.options.shared else "ReleaseStatic" 
        return platform, configuration
    
    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        
        self.copy("findHwloc.cmake", ".", ".")
        self.copy(pattern="*.h", dst="include", src="%s/include" % (self.ZIP_FOLDER_NAME), keep_path=True)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            platform, configuration = self.visual_platform_and_config()
            src = "%s/contrib/windows/%s/%s" % (self.ZIP_FOLDER_NAME, platform, configuration)
            
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=src, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src=src, keep_path=False)

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
        if self.settings.os == "Linux":
            self.cpp_info.libs = ["hwloc", "udev", "xml2"]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = ['hwloc']
        elif self.settings.os == "Windows":
            if self.options.shared: 
                self.cpp_info.libs = ["libhwloc"]
            else:
                self.cpp_info.libs = ["libhwloc-5"]
