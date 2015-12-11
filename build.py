import os
import platform
import sys

if __name__ == "__main__":
    os.system('conan export lasote/stable')
   
    def test(settings):
        argv =  " ".join(sys.argv[1:])
        command = "conan test %s %s" % (settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t %s" % command)


    if platform.system() == "Windows":
        print("It will fail first time because of adjustement of visual project. Open 'sln' project in hwloc\1.11.1\lasote\stable\source\hwloc-1.11.1\contrib/windows, update the solution and add x86 as configuration available ")
        raw_input("Press Enter to continue...")
        
        for compiler_version in ("12",):
            compiler = '-s compiler="Visual Studio" -s compiler.version=%s ' % compiler_version
            # Static x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o hwloc:shared=False')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o hwloc:shared=False')
    
            # Static x86_64
            test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o hwloc:shared=False')
            test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o hwloc:shared=False')
    
            # Shared x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o hwloc:shared=True')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o hwloc:shared=True')
    
            # Shared x86_64
            test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o hwloc:shared=True')
            test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o hwloc:shared=True')

    else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)
        if not os.getenv("TRAVIS", False):  
            # Static x86
            test('-s arch=x86 -s build_type=Debug -o hwloc:shared=False')
            test('-s arch=x86 -s build_type=Release -o hwloc:shared=False')
    
            # Shared x86
            test('-s arch=x86 -s build_type=Debug -o hwloc:shared=True')
            test('-s arch=x86 -s build_type=Release -o hwloc:shared=True')

        # Static x86_64
        test('-s arch=x86_64 -s build_type=Debug -o hwloc:shared=False')
        test('-s arch=x86_64 -s build_type=Release -o hwloc:shared=False')

        # Shared x86_64
        test('-s arch=x86_64 -s build_type=Debug -o hwloc:shared=True')
        test('-s arch=x86_64 -s build_type=Release -o hwloc:shared=True')
