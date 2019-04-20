# scons build for calc C++ library
import os, shutil, platform, re

import SCons.Builder

mxmlBuilder = SCons.Builder.Builder( action = 'mxmlc $SOURCE -output $TARGET' )

def renameDynamicLib(target, source, env):
   shutil.move( str(source[0]), str(target[0]) )
   return

env = Environment()

#paths
env.Append( ENV = {'PATH' : os.environ['PATH'] })
env.Append( BUILDERS = {'BuildMXML': mxmlBuilder} )

if(platform.system() == "Linux"):
   
   env.Append( CPPPATH = ['/usr/include/python3.5'] )
   env.Append( LIBPATH = ['/usr/lib/python3.5'] )

   env.Append( CPPFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )
   env.Append( LINKFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )

   env.Append( LIBS = [ 'boost_python' ] )

elif(platform.system() == "Windows"):
   env.Append( CPPPATH = [ Dir('C:/boost_1_70_0')] )
   env.Append( LIBPATH = [ Dir('C:/boost_1_70_0/stage/lib')] )

   env.Append( CPPFLAGS = ' /EHsc /MD /D "WIN64" /D "_CONSOLE" /W4 /Wall' )
else:
   print (platform.system() + " not supported")

#build engine tests
testExec = env.Program( target = 'test', source = ['src/server/engine/Board.cpp', 'src/server/engine/GameState.cpp', 'src/server/engine/tests/tests.cpp'] )

if(platform.system() == "Linux"):
   target = 'test'
   execution=env.Command("test --log_level=test_suite >&2", None, "./test --log_level=test_suite >&2")
elif(platform.system() == "Windows"):
   target = 'test.exe'
   execution=env.Command("test --log_level=test_suite", None, "test --log_level=test_suite")

Depends( execution,testExec )

#append python in order to compile boost python modules
if(platform.system() == "Linux"):
   env.Replace( LIBPATH = [] )
   env.Replace( LIBS = [ 'boost_unit_test_framework' ] )

elif(platform.system() == "Windows"):
   env.Append( CPPPATH = [ Dir('C:/Python37/include') ] )
   env.Append( LIBPATH = [ Dir('C:/Python37/libs') ] )
else:
   print (platform.system() + " not supported")

#build C++ library
cpplib = env.SharedLibrary( target = 'src/server/engine', source = ['src/server/engine/Board.cpp', 'src/server/engine/GameState.cpp', 'src/server/engine/module.cpp'] )

if(platform.system() == "Linux"):
   target = 'src/server/engine.so'
   env.Command( target, cpplib, renameDynamicLib )
elif(platform.system() == "Windows"):
   target = 'src/server/engine.pyd'
   env.Command( target, cpplib, renameDynamicLib )

