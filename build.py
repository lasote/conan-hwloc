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
        compiler = '-s compiler="Visual Studio" -s compiler.version=12 '
        # Static x86
        test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=False')
        test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=False')
        test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=False')
        test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=False')

        # Static x86_64
        test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=False')
        test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=False')
        test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=False')
        test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=False')

        # Shared x86
        test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=True')
        test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=True')
        test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=True')
        test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=True')

        # Shared x86_64
        test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=True')
        test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=True')
        test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=True')
        test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=True')

    else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)
        if not os.getenv("TRAVIS", False):  
            # Static x86
            test('-s arch=x86 -s build_type=Debug -o zlib:shared=False')
            test('-s arch=x86 -s build_type=Release -o zlib:shared=False')
    
            # Shared x86
            test('-s arch=x86 -s build_type=Debug -o zlib:shared=True')
            test('-s arch=x86 -s build_type=Release -o zlib:shared=True')

        # Static x86_64
        test('-s arch=x86_64 -s build_type=Debug -o zlib:shared=False')
        test('-s arch=x86_64 -s build_type=Release -o zlib:shared=False')

        # Shared x86_64
        test('-s arch=x86_64 -s build_type=Debug -o zlib:shared=True')
        test('-s arch=x86_64 -s build_type=Release -o zlib:shared=True')
