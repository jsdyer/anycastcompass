import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source import instance,province
class SourceTests(unittest.TestCase):
 def test_only_hostname_bind_txt_is_instance_evidence(self):
  self.assertEqual(instance({'answers':[{'TYPE':'TXT','NAME':'hostname.bind.','RDATA':['part','two']}]}),'parttwo');self.assertIsNone(instance({'answers':[{'TYPE':'TXT','NAME':'example.com','RDATA':['wrong']}]}));self.assertEqual(province(None,[]),'Unknown')
