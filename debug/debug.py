# coding=utf-8
from __future__ import unicode_literals, print_function

import argparse
import io
import json
import os
from builtins import input, bytes

from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.pipeline.configs.nlu_engine import NLUEngineConfig


def debug_training(dataset_path, config_path=None):
    with io.open(os.path.abspath(dataset_path), "r", encoding="utf8") as f:
        dataset = json.load(f)

    load_resources(dataset["language"])

    if config_path is None:
        config = NLUEngineConfig()
    else:
        with io.open(config_path, "r", encoding="utf8") as f:
            config = NLUEngineConfig.from_dict(json.load(f))

    engine = SnipsNLUEngine(config).fit(dataset)

    while True:
        query = input("Enter a query (type 'q' to quit): ").strip()
        if isinstance(query, bytes):
            query = query.decode("utf8")
        if query == "q":
            break
        print(json.dumps(engine.parse(query), indent=2))


def debug_inference(engine_path):
    with io.open(os.path.abspath(engine_path), "r", encoding="utf8") as f:
        engine_dict = json.load(f)

    load_resources(engine_dict["dataset_metadata"]["language_code"])
    engine = SnipsNLUEngine.from_dict(engine_dict)

    while True:
        query = input("Enter a query (type 'q' to quit): ").strip()
        if isinstance(query, bytes):
            query = query.decode("utf8")
        if query == "q":
            break
        print(json.dumps(engine.parse(query), indent=2))


def main_debug():
    parser = argparse.ArgumentParser(description="Debug snippets")
    parser.add_argument("mode", type=bytes,
                        choices=["training", "inference"],
                        help="'training' to debug training and 'inference to "
                             "debug inference'")
    parser.add_argument("path", type=bytes,
                        help="Path to the dataset or trained assistant")
    parser.add_argument("--config-path", type=bytes,
                        help="Path to the assistant configuration")
    args = vars(parser.parse_args())
    mode = args.pop("mode")
    if mode == "training":
        debug_training(*list(args.values()))
    elif mode == "inference":
        args.pop("config_path")
        debug_inference(*list(args.values()))
    else:
        raise ValueError("Invalid mode %s" % mode)


if __name__ == '__main__':
    main_debug()
