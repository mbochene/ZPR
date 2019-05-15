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
   env.Append( CPPFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )
   env.Append( LINKFLAGS = '-O2 -Wall -Wextra -pedantic -std=c++11' )
   env.Append( LIBS = [ 'boost_unit_test_framework' ] )

elif(platform.system() == "Windows"):
   env.Append( CPPPATH = [ Dir('C:/boost_1_70_0')] )
   env.Append( LIBPATH = [ Dir('C:/boost_1_70_0/stage/lib')] )

   env.Append( CPPFLAGS = ' /EHsc /MD /D "WIN64" /D "_CONSOLE" /W4 /Wall' )
else:
   print (platform.system() + " not supported")

#build engine tests
testExec = env.Program( target = 'test', source = ['src/server/engine/Board.cpp', 'src/server/engine/GameState.cpp', 'src/server/engine/tests/tests.cpp'] )

#append python in order to compile boost python modules
if(platform.system() == "Linux"):
   env.Append( CPPPATH = ['venv/include/python3.5m'] )
   env.Append( LIBPATH = ['venv/lib/python3.5'] )
   env.Append( LIBS = [ 'python3.5m', 'pthread', 'dl', 'util', 'm', 'libboost_python-py35' ] )

elif(platform.system() == "Windows"):
   env.Append( CPPPATH = [ Dir('C:/Python37/include') ] )
   env.Append( LIBPATH = [ Dir('C:/Python37/libs') ] )
else:
   print (platform.system() + " not supported")

#build C++ library
cpplib = env.SharedLibrary( target = 'src/server/engine', source = ['src/server/engine/Board.cpp', 'src/server/engine/GameState.cpp', 'src/server/engine/module.cpp'] )

if(platform.system() == "Linux"):
   target1 = 'src/server/engine.so'
   target2 = 'scripts/Linux/test'
elif(platform.system() == "Windows"):
   target1 = 'src/server/engine.pyd'
   target2 = 'scripts/Windows/test.exe'

env.Command( target1, cpplib, renameDynamicLib )
env.Command( target2, testExec, renameDynamicLib )
