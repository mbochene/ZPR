# scons build for calc C++ library
import os, shutil, platform, re

import SCons.Builder

mxmlBuilder = SCons.Builder.Builder( action = 'mxmlc $SOURCE -output $TARGET' )

def renameDynamicLib(target, source, env):
   shutil.move( str(source[0]), str(target[0]) )
   return

env = Environment()

#sciezki
env.Append( ENV = {'PATH' : os.environ['PATH'] })
env.Append( BUILDERS = {'BuildMXML': mxmlBuilder} )

if(platform.system() == "Linux"):
   
   env.Append( CPPPATH = ['/usr/include/python2.7'] )
   env.Append( LIBPATH = ['/usr/lib/python2.7'] )

   env.Append( CPPFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )
   env.Append( LINKFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )

   env.Append( LIBS = [ 'boost_python' ] )

elif(platform.system() == "Windows"):
   env.Append( CPPPATH = [ Dir('C:/Boost/include/boost-1_52'), #tutaj zainstalowane naglowki boost
                           Dir('C:/Python27/include') ] ) #tutaj zaistalowane naglowki python
   env.Append( LIBPATH = [ Dir('C:/Boost/lib'), #tutaj sciezka do bibliotek boost
                           Dir('C:/Python27/libs') ] ) #tutaj sciezki do bibliotek python

   env.Append( CPPFLAGS = ' /EHsc /MD /D "WIN32" /D "_CONSOLE" /W4' )
   env.Append( LINKFLAGS = ' /SUBSYSTEM:WINDOWS ' )
else:
   print platform.system() + " not supported"

#build C++ library
cpplib = env.SharedLibrary( target = 'src/server/engine', source = ['src/server/engine/Board.cpp', 'src/server/engine/GameState.cpp', 'src/server/engine/module.cpp'] )

if(platform.system() == "Linux"):
   target = 'src/server/engine.so'
elif(platform.system() == "Windows"):
   target = 'src/server/engine.pyd'

env.Command( target, cpplib, renameDynamicLib )


if(platform.system() == "Linux"):
   
   env.Append( CPPPATH = ['/usr/include/boost/test'] )
   env.Append( LIBPATH = ['/usr/lib/x86_64-linux-gnu'] )

   env.Replace( CPPFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )
   env.Replace( LINKFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )

   env.Append( LIBS = [ 'boost_unit_test_framework' ] )

elif(platform.system() == "Windows"):
   env.Append( CPPPATH = [ Dir('C:/Boost/include/boost-1_52'), #tutaj zainstalowane naglowki boost
                           Dir('C:/Python27/include') ] ) #tutaj zaistalowane naglowki python
   env.Append( LIBPATH = [ Dir('C:/Boost/lib'), #tutaj sciezka do bibliotek boost
                           Dir('C:/Python27/libs') ] ) #tutaj sciezki do bibliotek python

#build engine tests
testExec = env.Program( target = 'test', source = ['src/server/engine/Board.cpp', 'src/server/engine/GameState.cpp', 'src/server/engine/tests/tests.cpp'] )

if(platform.system() == "Linux"):
   target = 'test'
   env.Command("test --log_level=test_suite >&2", None, "./test --log_level=test_suite >&2")
elif(platform.system() == "Windows"):
   target = 'test.exe'

AlwaysBuild( testExec )
