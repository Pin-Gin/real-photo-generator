"""No GPU or network needed; protect the submission boundary from regressions."""
import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import run_t020e_e03b as run
from validate_t020e_workflow import validate


class TestE03BSubmission(unittest.TestCase):
    def test_full_reference_contract_is_present(self):
        w = run.build_workflow('person.png', 'garment.jpg', 'mask.png')
        self.assertEqual(validate(w, 'person.png', 'garment.jpg'), [])
        self.assertEqual(w['11']['inputs']['image'], ['2', 0])
        self.assertEqual(w['13']['inputs']['image'], ['3', 0])
        self.assertEqual(w['13']['inputs']['attn_mask'], ['12', 0])
        self.assertEqual(w['15']['inputs']['latent_image'], ['14', 0])
        self.assertNotIn('VAEEncode', [n['class_type'] for n in w.values()])

    def test_missing_master_adapter_is_rejected(self):
        w = run.build_workflow('person.png', 'garment.jpg', 'mask.png')
        w['13']['inputs']['model'] = ['1', 0]
        self.assertIn('MASTER_IDENTITY_CONDITIONING_MISSING', validate(w, 'person.png', 'garment.jpg'))

    def test_missing_garment_adapter_is_rejected(self):
        w = run.build_workflow('person.png', 'garment.jpg', 'mask.png')
        w['15']['inputs']['model'] = ['11', 0]
        self.assertIn('GARMENT_CONDITIONING_MISSING', validate(w, 'person.png', 'garment.jpg'))

    def test_schema_rejects_missing_mandatory_adapter_field(self):
        w = {'12': {'class_type': 'IPAdapterAdvanced', 'inputs': {'model': ['11', 0]}}}
        with patch.object(run, 'get_json', return_value={'IPAdapterAdvanced': {'input': {'required': {'model': ['MODEL', {}], 'image': ['IMAGE', {}]}}}}):
            with self.assertRaisesRegex(RuntimeError, 'MISSING_REQUIRED_FIELD'):
                run.ensure_nodes(w)

    def test_schema_rejects_bad_enum(self):
        w = {'12': {'class_type': 'IPAdapterAdvanced', 'inputs': {'weight_type': 'INVALID'}}}
        with patch.object(run, 'get_json', return_value={'IPAdapterAdvanced': {'input': {'required': {'weight_type': [['linear', 'ease in'], {}]}}}}):
            with self.assertRaisesRegex(RuntimeError, 'INVALID_CHOICE'):
                run.ensure_nodes(w)

    def test_mask_dimensions_must_match(self):
        with tempfile.TemporaryDirectory() as t:
            a,b,c=[Path(t)/x for x in ('master.png','garment.png','mask.png')]
            Image.new('RGB',(752,1392)).save(a)
            Image.new('RGB',(300,700)).save(b)
            Image.new('L',(600,1000)).save(c)
            with self.assertRaisesRegex(RuntimeError,'MASK_SIZE_MISMATCH'):
                run.validate_inputs(a,b,c)

    def test_mock_endpoint_receives_one_prompt_after_preflight(self):
        with tempfile.TemporaryDirectory() as t:
            tmp=Path(t)
            a,b,c=[tmp/x for x in ('master.png','garment.jpg','mask.png')]
            Image.new('RGB',(752,1392), '#bdbdbd').save(a)
            Image.new('RGB',(410,700),'#9988bb').save(b)
            m=Image.new('RGB',(752,1392),'black')
            ImageDraw.Draw(m).rectangle((200,360,540,950),fill='white')
            m.save(c)
            uploaded={}
            posted=[]
            def fake_request(path,data=None,content_type=None):
                if path=='/upload/image':
                    match=re.search(rb'filename="([^"]+)"',data)
                    assert match, 'Missing multipart filename'
                    fname=match.group(1).decode('utf-8')
                    role=fname.split('_')[2]
                    uploaded[role]=fname
                    return json.dumps({'name':fname,'type':'input','subfolder':''}).encode()
                if path=='/prompt':
                    prompt=json.loads(data)
                    posted.append(prompt)
                    return b'{"prompt_id":"mock-prompt-id"}'
                raise AssertionError('Unknown endpoint: '+path)
            with patch.object(run, 'ensure_models'),patch.object(run, 'ensure_nodes'),patch.object(run, 'request_bytes',side_effect=fake_request):
                rc=run.main(['--master',str(a),'--garment',str(b),'--mask',str(c),'--output',str(tmp/'output')])
            self.assertEqual(rc,0)
            self.assertEqual(len(uploaded),3)
            self.assertEqual(len(posted),1)
            w=posted[0]['prompt']
            self.assertEqual(validate(w,uploaded['master'],uploaded['garment']),[])
            self.assertEqual(w['12']['inputs']['image'],uploaded['mask'])
            self.assertEqual(w['13']['inputs']['attn_mask'],['12',0])
            self.assertEqual(w['17']['inputs']['filename_prefix'],run.PREFIX)
            self.assertTrue((tmp/'output'/'T020E_E03B_dual_reference_api_prompt.json').exists())

    def test_preflight_rejection_cannot_queue(self):
        with tempfile.TemporaryDirectory() as t:
            tmp=Path(t)
            a,b,c=[tmp/x for x in ('master.png','garment.jpg','mask.png')]
            Image.new('RGB',(752,1392),'#aaaaaa').save(a)
            Image.new('RGB',(300,600),'#aabbcc').save(b)
            mask=Image.new('RGB',(752,1392),'black')
            ImageDraw.Draw(mask).rectangle((200,300,450,900),fill='white')
            mask.save(c)
            posts=[]
            original=run.build_workflow
            def broken_builder(m,g,k):
                w=original(m,g,k)
                w['15']['inputs']['model']=['11',0]
                return w
            def fake_request(path,data=None,content_type=None):
                if path=='/upload/image':
                    match=re.search(rb'filename="([^"]+)"',data)
                    return json.dumps({'name':match.group(1).decode()}).encode()
                posts.append(path)
                return b'{"prompt_id":"oops"}'
            with patch.object(run,'ensure_models'),patch.object(run,'build_workflow',side_effect=broken_builder),patch.object(run,'request_bytes',side_effect=fake_request):
                rc=run.main(['--master',str(a),'--garment',str(b),'--mask',str(c),'--output',str(tmp/'out')])
            self.assertEqual(rc,2)
            self.assertNotIn('/prompt',posts)


if __name__=='__main__':
    unittest.main()
