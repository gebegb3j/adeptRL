#!/usr/bin/env python
# Copyright (C) 2018 Heron Systems, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
             __           __
  ____ _____/ /__  ____  / /_
 / __ `/ __  / _ \/ __ \/ __/
/ /_/ / /_/ /  __/ /_/ / /_
\__,_/\__,_/\___/ .___/\__/
               /_/
Evaluate

Evaluates an agent after training. Computes N-episode average reward by
loading a saved model from each epoch. N-episode averages are computed by
running N env in parallel.

Usage:
    evaluate (--log-id-dir <path>) [options]
    evaluate (-h | --help)

Required:
    --log-id-dir <path>     Path to train logs (.../logs/<env-id>/<log-id>)

Options:
    --gpu-id <int>          CUDA device ID of GPU [default: 0]
    --nb-episode <int>      Number of episodes to average [default: 30]
    --seed <int>            Seed for random variables [default: 512]
    --custom-network <str>  Name of custom network class
"""
from absl import flags

from adept.container import EvalContainer
from adept.utils.script_helpers import parse_path
from adept.utils.util import DotDict
from adept.container import Init

# hack to use argparse for SC2
FLAGS = flags.FLAGS
FLAGS(['local.py'])


def parse_args():
    from docopt import docopt
    args = docopt(__doc__)
    args = {k.strip('--').replace('-', '_'): v for k, v in args.items()}
    del args['h']
    del args['help']
    args = DotDict(args)
    args.log_id_dir = parse_path(args.log_id_dir)
    args.gpu_id = int(args.gpu_id)
    args.nb_episode = int(args.nb_episode)
    args.seed = int(args.seed)
    return args


MODE = 'Eval'


def main(args):
    """
    Run an evaluation.
    :param args: Dict[str, Any]
    :param agent_registry: AgentRegistry
    :param env_registry: EnvRegistry
    :param net_registry: NetworkRegistry
    :return:
    """
    args = DotDict(args)

    Init.print_ascii_logo()
    logger = Init.setup_logger(MODE, args.log_id_dir, 'eval')
    Init.log_args(logger, args)

    eval_container = EvalContainer(
        logger,
        args.log_id_dir,
        args.gpu_id,
        args.nb_episode,
        args.seed
    )
    try:
        eval_container.run()
    finally:
        eval_container.close()


if __name__ == '__main__':
    main(parse_args())
