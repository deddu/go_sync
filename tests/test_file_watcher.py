__author__ = 'deddu'
import file_watcher as fw
def test_addremotes():
    res=fw.addremotes([{'src_path':'./ciao/mondo.txt'}],'hello/world/')
    print res
    assert(res==[{'src_path':'./ciao/mondo.txt', 'remote_path':'hello/world/mondo.txt'}])
    res=fw.addremotes([{'src_path':'./ciao/bimbo/mondo.txt'}],'hello/world/')
    assert(res==[{'src_path':'./ciao/bimbo/mondo.txt', 'remote_path':'hello/world/mondo.txt'}])

