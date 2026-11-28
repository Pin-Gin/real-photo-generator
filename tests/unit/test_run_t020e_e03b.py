"""No GPU or network needed; protect the submission boundary from regressions."""
import copy
import json
import re
import sys
import tempfile
import subprocess
import shutil
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

    def test_isolated_python_imports_sibling_validator(self):
        # Reproduces the isolated sys.path behavior of ComfyUI embedded Python.
        runner = Path(__file__).resolve().parents[2] / 'scripts' / 'run_t020e_e03b.py'
        proc = subprocess.run([sys.executable, '-I', '-s', str(runner), '--help'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn('--dry-run', proc.stdout)

    def test_missing_validator_is_explicitly_rejected(self):
        runner = Path(__file__).resolve().parents[2] / 'scripts' / 'run_t020e_e03b.py'
        with tempfile.TemporaryDirectory() as t:
            destination = Path(t) / 'run_t020e_e03b.py'
            shutil.copyfile(runner, destination)
            proc = subprocess.run([sys.executable, '-I', '-s', str(destination), '--help'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, timeout=30)
            self.assertEqual(proc.returncode, 2, msg=proc.stdout + proc.stderr)
            self.assertIn('REJECT: VALIDATOR_FILE_MISSING', proc.stderr)

    def test_known_failed_e03b_never_queues_or_uploads(self):
        # QA FAIL must block BEFORE network calls, regardless of valid input paths.
        with patch.object(run, 'request_bytes', side_effect=AssertionError('network accessed')):
            rc=run.main(['--master','master.png','--garment','garment.jpg',
                         '--mask','mask.png','--output','outputs'])
        self.assertEqual(rc,2)

    def test_known_failed_e03b_dry_run_also_rejected(self):
        # Even dry-run should not upload images for this retired experiment.
        with patch.object(run, 'request_bytes', side_effect=AssertionError('network accessed')):
            rc=run.main(['--master','master.png','--garment','garment.jpg',
                         '--mask','mask.png','--output','outputs','--dry-run'])
        self.assertEqual(rc,2)


if __name__=='__main__':
    unittest.main()
