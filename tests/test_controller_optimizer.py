import pytest

from core.command import command_factory
from core.ssd_controller import SSDController
from core.buff_optimizer import Optimizer

DEFAULT_VALUE = '0x00000000'
cases_cls = [
    {  # 1
        'buff': [
            command_factory('E', 0, 10),
            command_factory('W', 5, '0x00000001')
        ],
        'optimized': [
            command_factory('E', 0, 5),
            command_factory('W', 5, '0x00000001'),
            command_factory('E', 6, 4)
        ],
    },
    {  # 2
        'buff': [
            command_factory('E', 0, 10),
            command_factory('W', 5, '0x00000001'),
            command_factory('W', 7, '0x00000001'),
        ],
        'optimized': [
            command_factory('E', 0, 5),
            command_factory('W', 5, '0x00000001'),
            command_factory('E', 6, 1),
            command_factory('W', 7, '0x00000001'),
            command_factory('E', 8, 2),
        ],
    },
    {  # 3
        'buff': [
            command_factory('E', 0, 4),
            command_factory('E', 4, 5)
        ],
        'optimized': [
            command_factory('E', 0, 9),
        ],
    },
    {  # 4
        'buff': [
            command_factory('W', 0, '0x0000000a'),
            command_factory('W', 0, '0x0000000b'),
        ],
        'optimized': [
            command_factory('W', 0, '0x0000000b'),
        ],
    },
    {  # 5
        'buff': [
            command_factory('E', 0, 3),
            command_factory('W', 4, '0x0000000a'),
            command_factory('E', 0, 5),

        ],
        'optimized': [
            command_factory('E', 0, 5),
        ],
    },
{  # 6
        'buff': [
            command_factory('W', 20, '0x0000000a'),
            command_factory('E', 10, 4),
            command_factory('E', 12, 3),

        ],
        'optimized': [
            command_factory('E', 10, 5),
            command_factory('W', 20, '0x0000000a'),
        ],
    },
    {  # 7
        'buff': [
            command_factory('E', 1, 1),
            command_factory('E', 3, 1),
            command_factory('E', 5, 1),
            command_factory('E', 7, 1),
            command_factory('E', 9, 1),
        ],
        'optimized': [
            command_factory('E', 1, 1),
            command_factory('E', 3, 1),
            command_factory('E', 5, 1),
            command_factory('E', 7, 1),
            command_factory('E', 9, 1),
        ],
    },
    {  # 8
        'buff': [
            command_factory('W', 1, DEFAULT_VALUE),
            command_factory('W', 3, DEFAULT_VALUE),
            command_factory('W', 5, DEFAULT_VALUE),
            command_factory('W', 7, DEFAULT_VALUE),
            command_factory('W', 9, DEFAULT_VALUE),
        ],
        'optimized': [
            command_factory('E', 1, 1),
            command_factory('E', 3, 1),
            command_factory('E', 5, 1),
            command_factory('E', 7, 1),
            command_factory('E', 9, 1),
        ],
    },
    {  # 9
        'buff': [
            command_factory('W', 1, '1'),
            command_factory('W', 2, '1'),
            command_factory('W', 3, '1'),
            command_factory('W', 4, '1'),
            command_factory('W', 5, '1'),
        ],
        'optimized': [
            command_factory('W', 1, '1'),
            command_factory('W', 2, '1'),
            command_factory('W', 3, '1'),
            command_factory('W', 4, '1'),
            command_factory('W', 5, '1'),
        ],
    },
]


def make_temp_cache(cmds) -> dict:
    cache_temp = {}
    for cmd in cmds:
        if cmd.mode == 'E':
            for i in range(cmd.lba, cmd.lba + cmd.size):
                cache_temp[i] = DEFAULT_VALUE
        if cmd.mode == 'W':
            cache_temp[cmd.lba] = cmd.value
    return cache_temp


@pytest.fixture
def optimizer():
    return Optimizer()


def test_controller_buffer_optimize_method_is_exist(optimizer):
    assert hasattr(optimizer, 'generate_new_commands')


@pytest.mark.parametrize("buff_cmd, optimized_cmd", [(case['buff'], case['optimized']) for case in cases_cls])
def test_controller_pick_smaller_commands(optimizer, buff_cmd, optimized_cmd):
    picked = buff_cmd
    if len(optimized_cmd) < len(buff_cmd):
        picked = optimized_cmd
    assert optimizer._pick_smaller_commands(optimized_cmd, buff_cmd) == picked


@pytest.mark.parametrize("buff_cmd, optimized_cmd_class", [(case['buff'], case['optimized']) for case in cases_cls])
def test_controller_generate_commands_method(optimizer, buff_cmd, optimized_cmd_class):
    temp_cache = make_temp_cache(buff_cmd)
    actual = optimizer.generate_new_commands(temp_cache)
    assert actual == optimized_cmd_class
