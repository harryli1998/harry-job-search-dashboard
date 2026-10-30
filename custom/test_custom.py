from pathlib import Path
from datetime import date
import json
import unittest
import search_plan
import workspace

ROOT=Path(__file__).resolve().parents[1]
class CustomTests(unittest.TestCase):
    def test_profile_drives_plan(self):
        p=json.loads((ROOT/'config/search-profile.example.json').read_text())
        plan=search_plan.build(p,date(2026,10,30))
        self.assertEqual(len(plan['queries']),30)
        self.assertEqual(plan['timezone'],'America/Los_Angeles')
        self.assertTrue(all(q['status']=='not_run' for q in plan['queries']))
        self.assertFalse(any('PhD' in q['query'] or 'Research Scientist' in q['query'] for q in plan['queries']))
        p['role_families']={'custom':['Pricing Analyst']}
        plan=search_plan.build(p,date(2026,10,30))
        self.assertTrue(all('Pricing Analyst' in q['query'] for q in plan['queries']))
    def test_demo_and_privacy_boundary(self):
        text=(ROOT/'demo/index.html').read_text()
        self.assertIn('公司、申请、面试和结果均为虚构示例',text)
        self.assertIn('var TABS = ["today", "discovered", "todo", "progress"];',text)
        for secret in ['@gmail.com','stem_extension_applied','private-secret-marker']:
            self.assertNotIn(secret,text)
    def test_init_preserves_existing(self):
        before=(ROOT/'.local/private/profile.json').read_bytes()
        with self.assertRaises(SystemExit): workspace.private_init()
        self.assertEqual((ROOT/'.local/private/profile.json').read_bytes(),before)
if __name__=='__main__': unittest.main()
