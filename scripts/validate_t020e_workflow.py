#!/usr/bin/env python3
"""Fail-closed structural preflight for T-020E garment generation workflows.

Scope: new-latent workflows with separately connected identity, garment, pose.
This is not an image-quality assessor. No API calls, file writes, or generation.
"""
import argparse
import json
import sys
from pathlib import Path


def link_node(value):
    return str(value[0]) if isinstance(value, list) and len(value) == 2 and isinstance(value[0], (str, int)) and isinstance(value[1], int) else None


def ancestors(graph, start):
    found, pending = set(), [str(start)]
    while pending:
        key = pending.pop()
        if key in found or key not in graph:
            continue
        found.add(key)
        for value in graph[key].get('inputs', {}).values():
            nxt = link_node(value)
            if nxt:
                pending.append(nxt)
    return found


def from_image(graph, link, source_id):
    node_id = link_node(link)
    return node_id is not None and source_id in ancestors(graph, node_id)


def validate(data, master_name, garment_name):
    errors = []
    graph = data.get('prompt', data) if isinstance(data, dict) else {}
    if not isinstance(graph, dict) or not graph:
        return ['NOT_API_PROMPT_JSON']
    if not all(isinstance(n, dict) and 'class_type' in n and isinstance(n.get('inputs', {}), dict) for n in graph.values()):
        return ['INVALID_NODE_FORMAT']

    def nodes(kind):
        return [(str(nid), node) for nid, node in graph.items() if node.get('class_type') == kind]

    samplers = nodes('KSampler')
    if len(samplers) != 1:
        return ['EXPECTED_SINGLE_KSAMPLER']
    _, sampler = samplers[0]
    ins = sampler['inputs']
    model = link_node(ins.get('model'))
    positive = link_node(ins.get('positive'))
    latent = link_node(ins.get('latent_image'))
    if not model or not positive or not latent:
        return ['SAMPLER_MISSING_MODEL_POSITIVE_OR_LATENT']
    model_path, pos_path, latent_path = ancestors(graph, model), ancestors(graph, positive), ancestors(graph, latent)
    latent_nodes = {graph[n]['class_type'] for n in latent_path}
    if 'EmptyLatentImage' not in latent_nodes:
        errors.append('NO_EMPTY_LATENT_GENERATION')
    if latent_nodes.intersection({'VAEEncode', 'VAEEncodeForInpaint', 'InpaintModelConditioning', 'SetLatentNoiseMask', 'LatentCompositeMasked'}):
        errors.append('SOURCE_IMAGE_EDIT_LATENT_FORBIDDEN')

    master_loaders = [nid for nid, node in nodes('LoadImage') if node['inputs'].get('image') == master_name]
    garment_loaders = [nid for nid, node in nodes('LoadImage') if node['inputs'].get('image') == garment_name]
    if master_name == garment_name:
        errors.append('MASTER_AND_GARMENT_MUST_DIFFER')
    if not master_loaders:
        errors.append('MASTER_LOAD_IMAGE_MISSING')
    if not garment_loaders:
        errors.append('GARMENT_LOAD_IMAGE_MISSING')
    if not master_loaders or not garment_loaders:
        return errors

    # A Master image entering OpenPose is NOT an identity reference.
    identity = False
    garments = False
    for nid, node in graph.items():
        typ = node['class_type']
        if typ == 'IPAdapterAdvanced' and str(nid) in model_path and isinstance(node['inputs'].get('weight'), (int, float)) and node['inputs']['weight'] > 0 and node['inputs'].get('start_at', 0) < node['inputs'].get('end_at', 1):
            for mid in master_loaders:
                identity |= from_image(graph, node['inputs'].get('image'), mid)
            for gid in garment_loaders:
                garments |= from_image(graph, node['inputs'].get('image'), gid)
        if typ == 'TextEncodeQwenImageEditPlus' and str(nid) in pos_path:
            for mid in master_loaders:
                identity |= from_image(graph, node['inputs'].get('image1'), mid)
            for gid in garment_loaders:
                garments |= from_image(graph, node['inputs'].get('image2'), gid)
    if not identity:
        errors.append('MASTER_IDENTITY_CONDITIONING_MISSING')
    if not garments:
        errors.append('GARMENT_CONDITIONING_MISSING')

    # Pose control is only a structural minimum, NOT body-size preservation.
    pose_nodes = {nid for nid, node in nodes('OpenposePreprocessor') if any(from_image(graph, node['inputs'].get('image'), mid) for mid in master_loaders)}
    pose_used = any(nid in pos_path and isinstance(node['inputs'].get('strength'), (int, float)) and node['inputs']['strength'] > 0 and node['inputs'].get('start_percent', 0) < node['inputs'].get('end_percent', 1) and from_image(graph, node['inputs'].get('image'), p) for nid, node in nodes('ControlNetApplyAdvanced') for p in pose_nodes)
    if not pose_used:
        errors.append('MASTER_POSE_CONDITIONING_MISSING')
    return errors


def main():
    p = argparse.ArgumentParser(description='T-020E preflight: reject missing generation references')
    p.add_argument('--workflow', required=True, type=Path)
    p.add_argument('--master', required=True, help='Exact ComfyUI LoadImage.inputs.image filename')
    p.add_argument('--garment', required=True, help='Exact ComfyUI LoadImage.inputs.image filename')
    args = p.parse_args()
    try:
        data = json.loads(args.workflow.read_text(encoding='utf-8-sig'))
        faults = validate(data, args.master, args.garment)
    except (OSError, ValueError, UnicodeError) as exc:
        print('REJECT: WORKFLOW_UNREADABLE: ' + str(exc))
        return 2
    if faults:
        for fault in faults:
            print('REJECT: ' + fault)
        return 2
    print('STRUCTURAL_PRECHECK_PASS (NOT IMAGE QA PASS)')
    print('WARNING: Master body ratios, garment isolation, wearing physics, mannequin transfer, and output quality remain UNVERIFIED.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
