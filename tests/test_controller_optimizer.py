import pytest

from core.command import WriteCommand, EraseCommand
from core.ssd_controller import SSDController
from dataclasses import dataclass

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
            EraseCommand('E', 0, 5),
            WriteCommand('W', 5, '0x00000001'),
            EraseCommand('E', 6, 4)
        ],
    },
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '0x00000001'),
            ('W', 7, '0x00000001'),
        ],
        'optimized': [
            EraseCommand('E', 0, 5),
            WriteCommand('W', 5, '0x00000001'),
            EraseCommand('E', 6, 1),
            WriteCommand('W', 7, '0x00000001'),
            EraseCommand('E', 8, 2),
        ],
    },
    {
        'buff': [
            ('E', 0, 4),
            ('E', 4, 5)
        ],
        'optimized': [
            EraseCommand('E', 0, 9),
        ],
    },
    {
        'buff': [
            ('W', 0, '0x0000000a'),
            ('W', 0, '0x0000000b'),
        ],
        'optimized': [
            WriteCommand('W', 0, '0x0000000b'),
        ],
    },
    {
        'buff': [
            ('E', 0, 3),
            ('W', 4, '0x0000000a'),
            ('E', 0, 5),

        ],
        'optimized': [
            EraseCommand('E', 0, 5),
        ],
    },
    {
        'buff': [
            ('W', 20, '0x0000000a'),
            ('E', 10, 4),
            ('E', 12, 3),

        ],
        'optimized': [
            EraseCommand('E', 10, 5),
            WriteCommand('W', 20, '0x0000000a'),
        ],
    },
]

DEFAULT_VALUE = '0x00000000'
캐시사이즈 = 100


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
    assert controller._generate_commands(temp_cache) == optimized_cmd_class
