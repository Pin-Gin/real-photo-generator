"""Stdlib regression tests for T-020E's previously missed structural defects."""
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from validate_t020e_workflow import validate

MASTER = 'master_candidate_01.png'
GARMENT = 'garment_reference.jpg'


def make_graph(garment=True, pose=True, edit_latent=False):
    g = {
        '1': {'class_type': 'LoadImage', 'inputs': {'image': MASTER}},
        '2': {'class_type': 'LoadImage', 'inputs': {'image': GARMENT}},
        '3': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'RealVisXL_V5.0_fp16.safetensors'}},
        '4': {'class_type': 'CLIPTextEncode', 'inputs': {'clip': ['3', 1], 'text': 'worn clothing'}},
        '5': {'class_type': 'CLIPTextEncode', 'inputs': {'clip': ['3', 1], 'text': 'negative'}},
        '6': {'class_type': 'EmptyLatentImage', 'inputs': {'width': 768, 'height': 1344, 'batch_size': 1}},
        '7': {'class_type': 'OpenposePreprocessor', 'inputs': {'image': ['1', 0]}},
        '8': {'class_type': 'ControlNetLoader', 'inputs': {'control_net_name': 'SDXL/OpenPose'}},
        '9': {'class_type': 'ControlNetApplyAdvanced', 'inputs': {
            'positive': ['4', 0], 'negative': ['5', 0], 'control_net': ['8', 0],
            'image': ['7', 0], 'strength': 0.85, 'start_percent': 0., 'end_percent': 1.}},
        '10': {'class_type': 'IPAdapterAdvanced', 'inputs': {
            'model': ['3', 0], 'image': ['1', 0], 'ipadapter': ['20', 0],
            'weight': 0.6, 'start_at': 0, 'end_at': 1}},
        '11': {'class_type': 'IPAdapterAdvanced', 'inputs': {
            'model': ['10', 0], 'image': ['2', 0], 'ipadapter': ['20', 0],
            'weight': 0.6, 'start_at': 0, 'end_at': 1}},
        '20': {'class_type': 'IPAdapterModelLoader', 'inputs': {
            'ipadapter_file': 'ip-adapter-plus_sdxl_vit-h.safetensors'}},
        '12': {'class_type': 'KSampler', 'inputs': {
            'model': ['11', 0], 'positive': ['9', 0], 'negative': ['9', 1], 'latent_image': ['6', 0]}}
    }
    if not garment:
        g['12']['inputs']['model'] = ['10', 0]
    if not pose:
        g['12']['inputs']['positive'] = ['4', 0]
    if edit_latent:
        g['13'] = {'class_type': 'VAEEncode', 'inputs': {'pixels': ['1', 0], 'vae': ['3', 2]}}
        g['12']['inputs']['latent_image'] = ['13', 0]
    return g


class TestT020EContract(unittest.TestCase):
    def test_e03a_style_pipeline_rejected(self):
        g = make_graph()
        g['12']['inputs']['model'] = ['3', 0]  # pose and text only: E-03A defect
        faults = validate(g, MASTER, GARMENT)
        self.assertIn('MASTER_IDENTITY_CONDITIONING_MISSING', faults)
        self.assertIn('GARMENT_CONDITIONING_MISSING', faults)

    def test_missing_garment_rejected(self):
        self.assertIn('GARMENT_CONDITIONING_MISSING',
                      validate(make_graph(garment=False), MASTER, GARMENT))

    def test_missing_pose_rejected(self):
        self.assertIn('MASTER_POSE_CONDITIONING_MISSING',
                      validate(make_graph(pose=False), MASTER, GARMENT))

    def test_source_image_edit_latent_rejected(self):
        faults = validate(make_graph(edit_latent=True), MASTER, GARMENT)
        self.assertIn('NO_EMPTY_LATENT_GENERATION', faults)
        self.assertIn('SOURCE_IMAGE_EDIT_LATENT_FORBIDDEN', faults)

    def test_missing_input_filename_rejected(self):
        self.assertIn('GARMENT_LOAD_IMAGE_MISSING',
                      validate(make_graph(), MASTER, 'wrong_garment.png'))

    def test_disabled_identity_adapter_rejected(self):
        g = make_graph()
        g['10']['inputs']['weight'] = 0
        self.assertIn('MASTER_IDENTITY_CONDITIONING_MISSING',
                      validate(g, MASTER, GARMENT))

    def test_disabled_pose_rejected(self):
        g = make_graph()
        g['9']['inputs']['strength'] = 0
        self.assertIn('MASTER_POSE_CONDITIONING_MISSING',
                      validate(g, MASTER, GARMENT))

    def test_structural_pass_is_not_wearing_quality_pass(self):
        self.assertEqual(validate(make_graph(), MASTER, GARMENT), [])


if __name__ == '__main__':
    unittest.main()
