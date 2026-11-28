#!/usr/bin/env python3
"""T020E E03B: structural gate -> ComfyUI validation -> at most one queued image.

No Git writes, no model installs, no Master edits, no generated image uploads to Git.
This is an experiment: two IP-Adapters cannot guarantee correct clothes/body.
"""
import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
import uuid

from PIL import Image

# The Windows ComfyUI embedded interpreter may not include this script's
# directory on sys.path (python*._pth isolated path configuration).
# Resolve the sibling validator explicitly rather than relying on sys.path.
_SCRIPT_DIR = Path(__file__).resolve().parent
_VALIDATOR_FILE = _SCRIPT_DIR / 'validate_t020e_workflow.py'
if not _VALIDATOR_FILE.is_file():
    print('REJECT: VALIDATOR_FILE_MISSING: ' + str(_VALIDATOR_FILE), file=sys.stderr)
    sys.exit(2)
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from validate_t020e_workflow import validate

API = 'http://127.0.0.1:8188'
CKPT = 'RealVisXL_V5.0_fp16.safetensors'
CN = r'SDXL\controlnet-openpose-sdxl-1.0\diffusion_pytorch_model.safetensors'
IPA = 'ip-adapter-plus_sdxl_vit-h.safetensors'
CLIPVISION = 'CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors'
PREFIX = 'T020E_E03B_SDXL_DualReference_Worn'

POSITIVE = (
    'High-quality semi-realistic 3D CGI to photorealistic portrait of one adult woman. '
    'Depict the SAME woman as the full-body person identity reference: identical face, hair cut and color, '
    'skin tone, body dimensions and height-to-head proportion, natural neck length, shoulders, torso, '
    'hips and limbs. Match the person reference standing posture and full body framing. '
    'Dress her in the EXACT lavender reference garment as a complete, physically worn outfit: '
    'the reference garment establishes the true cloth construction, cut, seams, sleeves, skirt layers, '
    'ruffles, bows, color, and transparent or sheer textile properties where present. '
    'The garment is sewn and worn, drapes under gravity, has appropriate openings and secure joins, '
    'fits and follows realistic human anatomy; cloth contact and fabric layering are plausible. '
    'Replace the original cream camisole and shorts completely; they are not worn under the new outfit. '
    'The garment display mannequin in the clothing reference is NOT a person or anatomy reference. '
    'Do not copy any transparent mannequin body, mannequin shoulders, neck, plastic reflections, or rigging. '
    'Natural living human skin and anatomy. Neutral simple studio interior. '
    'SFW, full-length head to bare feet, both feet visible, finely detailed CGI quality.'
)
NEGATIVE = (
    'different person, different face, different hairstyle, elongated neck, impossible head size, '
    'stretched torso, mannequin physique, glass body, transparent body, artificial plastic skin, '
    'detached limbs, extra hands, displaced shoulders, distorted ribcage, broken pelvis, '
    'clothes superimposed over old clothes, transparent old camisole, old shorts showing through, '
    'pasted flat texture, detached floating bows, outfit fragments, double clothing, '
    'incorrect garment construction, unnatural cloth connections, opaque replacement for sheer fabric, '
    'nude body, underwear-only, anime line art, comic style, cel shading, cropped body, blurry, low quality'
)


def request_bytes(path, data=None, content_type=None):
    headers = {} if content_type is None else {'Content-Type': content_type}
    req = urllib.request.Request(API + path, data=data, headers=headers, method='POST' if data is not None else 'GET')
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')[:3500]
        raise RuntimeError(f'HTTP_{exc.code} {path}: {body}') from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f'COMFYUI_UNAVAILABLE {path}: {exc}') from exc


def get_json(path):
    return json.loads(request_bytes(path))


def ensure_models():
    for category, expected in [('checkpoints', CKPT), ('controlnet', CN), ('ipadapter', IPA), ('clip_vision', CLIPVISION)]:
        entries = get_json('/models/' + category)
        if not isinstance(entries, list) or expected not in entries:
            raise RuntimeError(f'MODEL_NOT_FOUND category={category} required={expected!r} actual={entries!r}')


def ensure_nodes(workflow):
    cache = {}
    for node in workflow.values():
        kind, ins = node['class_type'], node['inputs']
        if kind not in cache:
            data = get_json('/object_info/' + kind)
            if kind not in data:
                raise RuntimeError('NODE_NOT_INSTALLED: ' + kind)
            cache[kind] = data[kind]
        spec = cache[kind].get('input', {})
        required = spec.get('required', {})
        for field, rule in required.items():
            if field not in ins:
                raise RuntimeError(f'MISSING_REQUIRED_FIELD {kind}.{field}')
            value = ins[field]
            if not isinstance(value, list) and isinstance(rule, list) and len(rule) and isinstance(rule[0], list):
                if value not in rule[0]:
                    raise RuntimeError(f'INVALID_CHOICE {kind}.{field}={value!r}, choices={rule[0]!r}')
        allowed = set(required) | set(spec.get('optional', {})) | set(spec.get('hidden', {}))
        unknown = set(ins) - allowed
        if unknown:
            raise RuntimeError(f'UNKNOWN_FIELDS {kind}: {sorted(unknown)}')


def upload_image(path, role):
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()[:12]
    extension = path.suffix.lower()
    target = f'T020E_E03B_{role}_{digest}{extension}'
    boundary = '----T020E' + uuid.uuid4().hex
    parts = []
    def field(name, value):
        parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode('utf-8'))
    field('type', 'input')
    field('overwrite', 'true')  # Content-hashed filename: retry-safe, never touches source files.
    mime = mimetypes.guess_type(target)[0] or 'application/octet-stream'
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{target}"\r\nContent-Type: {mime}\r\n\r\n').encode('utf-8') + content + b'\r\n')
    parts.append(f'--{boundary}--\r\n'.encode('utf-8'))
    uploaded = json.loads(request_bytes('/upload/image', b''.join(parts), f'multipart/form-data; boundary={boundary}'))
    name = uploaded.get('name')
    if not isinstance(name, str) or not name:
        raise RuntimeError(f'INVALID_UPLOAD_RESPONSE {role}: {uploaded!r}')
    return name


def validate_inputs(master, garment, mask):
    for role, path in [('MASTER', master), ('GARMENT', garment), ('MASK', mask)]:
        if not path.is_file():
            raise RuntimeError(f'{role}_NOT_FOUND: {path}')
    with Image.open(master) as im, Image.open(garment) as garment_image, Image.open(mask) as mask_image:
        if im.size != mask_image.size:
            raise RuntimeError(f'MASK_SIZE_MISMATCH master={im.size} mask={mask_image.size}')
        if garment_image.width < 128 or garment_image.height < 128:
            raise RuntimeError('GARMENT_IMAGE_TOO_SMALL')
        # LoadImageMask channel='red': verify mask's red channel varies.
        extrema = mask_image.convert('RGB').getchannel('R').getextrema()
        if extrema[0] == extrema[1]:
            raise RuntimeError('MASK_EMPTY_OR_SOLID')
    if master.resolve() == garment.resolve() or master.read_bytes() == garment.read_bytes():
        raise RuntimeError('MASTER_AND_GARMENT_NOT_DISTINCT')


def build_workflow(master, garment, mask):
    # It is a wholly new generation: Master is never routed to VAEEncode.
    return {
        '1': {'class_type':'CheckpointLoaderSimple','inputs': {'ckpt_name': CKPT}},
        '2': {'class_type':'LoadImage','inputs': {'image':master}},
        '3': {'class_type':'LoadImage','inputs': {'image':garment}},
        '4': {'class_type':'OpenposePreprocessor','inputs': {'image':['2',0]}},
        '5': {'class_type':'ControlNetLoader','inputs': {'control_net_name':CN}},
        '6': {'class_type':'CLIPTextEncode','inputs': {'clip':['1',1], 'text':POSITIVE}},
        '7': {'class_type':'CLIPTextEncode','inputs': {'clip':['1',1], 'text':NEGATIVE}},
        '8': {'class_type':'ControlNetApplyAdvanced','inputs': {
            'positive':['6',0], 'negative':['7',0], 'control_net':['5',0], 'image':['4',0],
            'strength':0.78, 'start_percent':0.0, 'end_percent':1.0}},
        '9': {'class_type':'IPAdapterModelLoader','inputs': {'ipadapter_file':IPA}},
        '10': {'class_type':'CLIPVisionLoader','inputs': {'clip_name':CLIPVISION}},
        '11': {'class_type':'IPAdapterAdvanced','inputs': {
            'model':['1',0], 'ipadapter':['9',0], 'image':['2',0], 'weight':0.85,
            'weight_type':'linear', 'combine_embeds':'concat','start_at':0.0,'end_at':1.0,
            'embeds_scaling':'V only', 'clip_vision':['10',0]}},
        '12': {'class_type':'LoadImageMask','inputs': {'image':mask,'channel':'red'}},
        '13': {'class_type':'IPAdapterAdvanced','inputs': {
            'model':['11',0], 'ipadapter':['9',0], 'image':['3',0], 'weight':0.58,
            'weight_type':'linear', 'combine_embeds':'concat','start_at':0.0,'end_at':1.0,
            'embeds_scaling':'V only', 'clip_vision':['10',0], 'attn_mask':['12',0]}},
        '14': {'class_type':'EmptyLatentImage','inputs': {'width':768,'height':1344,'batch_size':1}},
        '15': {'class_type':'KSampler','inputs': {
            'seed':2026112805,'steps':30,'cfg':5.5,'sampler_name':'dpmpp_2m',
            'scheduler':'karras','denoise':1.0,'model':['13',0],
            'positive':['8',0],'negative':['8',1],'latent_image':['14',0]}},
        '16': {'class_type':'VAEDecode','inputs': {'samples':['15',0],'vae':['1',2]}},
        '17': {'class_type':'SaveImage','inputs': {'images':['16',0],'filename_prefix':PREFIX}},
    }


def main(argv=None):
    p = argparse.ArgumentParser(description='Single gated SDXL dual-reference test (NOT a quality pass).')
    p.add_argument('--master', type=Path, required=True)
    p.add_argument('--garment', type=Path, required=True)
    p.add_argument('--mask', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True, help='Folder for JSON and execution receipt (not Git)')
    p.add_argument('--dry-run', action='store_true', help='Check and save prompt, but DO NOT queue')
    args=p.parse_args(argv)
    try:
        validate_inputs(args.master,args.garment,args.mask)
        ensure_models()
        up_master=upload_image(args.master,'master')
        up_garment=upload_image(args.garment,'garment')
        up_mask=upload_image(args.mask,'mask')
        workflow=build_workflow(up_master,up_garment,up_mask)
        errors=validate(workflow,up_master,up_garment)
        if errors:
            raise RuntimeError('STATIC_PREFLIGHT_REJECT: '+', '.join(errors))
        # Explicit mask constraint beyond the generic preflight.
        garment_node=workflow['13']['inputs']
        if garment_node.get('attn_mask') != ['12',0] or workflow['12']['inputs']['image'] != up_mask:
            raise RuntimeError('GARMENT_REGION_MASK_DISCONNECTED')
        print('STRUCTURAL_PRECHECK_PASS (NOT IMAGE QA PASS)')
        ensure_nodes(workflow)
        print('COMFYUI_NODE_SCHEMA_PASS (NOT MODEL EXECUTION PASS)')
        args.output.mkdir(parents=True,exist_ok=True)
        target=args.output/'T020E_E03B_dual_reference_api_prompt.json'
        prompt={'prompt':workflow,'client_id':'T020E_E03B_gated'}
        expected=json.dumps(prompt,ensure_ascii=False,indent=2)
        receipt=args.output/'T020E_E03B_receipt.json'
        if receipt.exists():
            raise RuntimeError('ALREADY_QUEUED_NO_DUPLICATE: '+str(receipt))
        if target.exists():
            if target.read_text(encoding='utf-8') != expected:
                raise RuntimeError('WORKFLOW_OUTPUT_DIFFERS_NO_OVERWRITE: '+str(target))
        else:
            target.write_text(expected,encoding='utf-8')
        print('WORKFLOW_SAVED: '+str(target))
        if args.dry_run:
            print('DRY_RUN_ONLY: NO_GENERATION_QUEUED')
            return 0
        response=json.loads(request_bytes('/prompt',json.dumps(prompt).encode('utf-8'),'application/json; charset=utf-8'))
        prompt_id=response.get('prompt_id')
        if not isinstance(prompt_id,str) or not prompt_id:
            raise RuntimeError('PROMPT_NOT_ACCEPTED: '+repr(response))
        receipt.write_text(json.dumps({'prompt_id':prompt_id,'prefix':PREFIX,'status':'QUEUED_NOT_QA'},indent=2),encoding='utf-8')
        print('QUEUED_ONE_IMAGE: '+prompt_id)
        print('OUTPUT_PREFIX: '+PREFIX)
        print('QA_STATUS: UNVERIFIED (do not infer PASS from queue acceptance)')
        return 0
    except (OSError, RuntimeError, ValueError, urllib.error.URLError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        return 2

if __name__=='__main__':
    sys.exit(main())
