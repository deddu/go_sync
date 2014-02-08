import api_interface as a
def test_transfer_single():
    res=a.transfer('this','that',"ep1","ep2")
    assert res
    assert res.source_endpoint == "ep1"
    assert res.destination_endpoint=="ep2"
    assert res.sync_level ==3
    assert len(res.items)>0
    assert res.items[0]['DATA_TYPE']== 'transfer_item'
    assert res.items[0]['source_path']== "this"
    assert res.items[0]['destination_path']== "that"

def test_transfer_multiple():
    res=a.transfer(['this1','this2'],['that1','that2'],"ep1","ep2")
    assert res
    assert res.source_endpoint == "ep1"
    assert res.destination_endpoint=="ep2"
    assert res.sync_level ==3
    assert len(res.items)>1
    assert res.items[0]['DATA_TYPE']== 'transfer_item'
    assert res.items[0]['source_path']== "this1"
    assert res.items[0]['destination_path']== "that1"

def test_transfer_exceptions():
     try:
        a.transfer(['this1','this2'],'that1',"ep1","ep2")
     except Exception as e:
        pass
     finally:
        assert e.message=="the formats of the source and destinations do not match."

     try:
        a.transfer(['this1','this2'],['that1'],"ep1","ep2")
     except Exception as e:
        pass
     finally:
        assert e.message=="the number of sources and destinations specified is not the same"