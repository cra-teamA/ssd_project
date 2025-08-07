import pytest

from core.command import command_factory
from core.ssd_controller import SSDController

DEFAULT_VALUE = '0x00000000'
캐시사이즈 = 100
cases = [
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '0x00000001')
        ],
        'optimized': [
            ('E', 0, 5),
            ('W', 5, '0x00000001'),
            ('E', 6, 4)
        ],
    },
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '0x00000001'),
            ('W', 7, '0x00000001'),
        ],
        'optimized': [
            ('E', 0, 5),
            ('W', 5, '0x00000001'),
            ('E', 6, 1),
            ('W', 7, '0x00000001'),
            ('E', 8, 2),
        ],
    },
    {
        'buff': [
            ('E', 0, 4),
            ('E', 4, 5)
        ],
        'optimized': [
            ('E', 0, 9),
        ],
    },
    {
        'buff': [
            ('W', 0, '0x0000000a'),
            ('W', 0, '0x0000000b'),
        ],
        'optimized': [
            ('W', 0, '0x0000000b'),
        ],
    },
    {
        'buff': [
            ('E', 0, 3),
            ('W', 4, '0x0000000a'),
            ('E', 0, 5),

        ],
        'optimized': [
            ('E', 0, 5),
        ],
    },
]

cases_cls = [
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '0x00000001')
        ],
        'optimized': [
            command_factory('E', 0, 5),
            command_factory('W', 5, '0x00000001'),
            command_factory('E', 6, 4)
        ],
    },
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '0x00000001'),
            ('W', 7, '0x00000001'),
        ],
        'optimized': [
            command_factory('E', 0, 5),
            command_factory('W', 5, '0x00000001'),
            command_factory('E', 6, 1),
            command_factory('W', 7, '0x00000001'),
            command_factory('E', 8, 2),
        ],
    },
    {
        'buff': [
            ('E', 0, 4),
            ('E', 4, 5)
        ],
        'optimized': [
            command_factory('E', 0, 9),
        ],
    },
    {
        'buff': [
            ('W', 0, '0x0000000a'),
            ('W', 0, '0x0000000b'),
        ],
        'optimized': [
            command_factory('W', 0, '0x0000000b'),
        ],
    },
    {
        'buff': [
            ('E', 0, 3),
            ('W', 4, '0x0000000a'),
            ('E', 0, 5),

        ],
        'optimized': [
            command_factory('E', 0, 5),
        ],
    },
    {
        'buff': [
            ('W', 20, '0x0000000a'),
            ('E', 10, 4),
            ('E', 12, 3),

        ],
        'optimized': [
            command_factory('E', 10, 5),
            command_factory('W', 20, '0x0000000a'),
        ],
    },
    {
        'buff': [
            ('E', 1, 1),
            ('E', 3, 1),
            ('E', 5, 1),
            ('E', 7, 1),
            ('E', 9, 1),
        ],
        'optimized': [
            command_factory('E', 1, 1),
            command_factory('E', 3, 1),
            command_factory('E', 5, 1),
            command_factory('E', 7, 1),
            command_factory('E', 9, 1),
        ],
    },
    {
        'buff': [
            ('W', 1, '1'),
            ('W', 3, '1'),
            ('W', 5, '1'),
            ('W', 7, '1'),
            ('W', 9, '1'),
        ],
        'optimized': [
            command_factory('W', 1, '1'),
            command_factory('W', 3, '1'),
            command_factory('W', 5, '1'),
            command_factory('W', 7, '1'),
            command_factory('W', 9, '1'),
        ],
    },
    {
        'buff': [
            ('W', 1, DEFAULT_VALUE),
            ('W', 2, DEFAULT_VALUE),
            ('W', 3, DEFAULT_VALUE),
            ('W', 4, DEFAULT_VALUE),
            ('W', 5, DEFAULT_VALUE),
        ],
        'optimized': [
            command_factory('E', 1, 5),
        ],
    },
]


def make_temp_cache(cmd) -> dict:
    cache_temp = {i: None for i in range(캐시사이즈)}
    for action_type, addr, c in cmd:
        if action_type == 'E':
            for i in range(addr, addr + c):
                cache_temp[i] = DEFAULT_VALUE
        if action_type == 'W':
            cache_temp[addr] = c
    return cache_temp


@pytest.fixture
def controller():
    return SSDController()


def test_controller_buffer_optimize_method_is_exist(controller):
    assert hasattr(controller, 'buffer_optimize')


@pytest.mark.parametrize("buff_cmd, optimized_cmd", [(case['buff'], case['optimized']) for case in cases])
def test_controller_pick_smaller_commands(controller, buff_cmd, optimized_cmd):
    picked = buff_cmd
    if len(optimized_cmd) < len(buff_cmd):
        picked = optimized_cmd
    assert controller._pick_smaller_commands(buff_cmd, optimized_cmd) == picked


@pytest.mark.parametrize("buff_cmd, optimized_cmd_class", [(case['buff'], case['optimized']) for case in cases_cls])
def test_controller_generate_commands_method(controller, buff_cmd, optimized_cmd_class):
    temp_cache = make_temp_cache(buff_cmd)
    controller.cache = temp_cache
    assert controller._generate_commands() == optimized_cmd_class
