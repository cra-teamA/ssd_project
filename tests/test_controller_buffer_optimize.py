import pytest
from core.ssd_controller import SSDController

cases = [
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '1')
        ],
        'optimized': [
            ('E', 0, 5),
            ('W', 5, '1'),
            ('E', 6, 4)
        ],
    },
    {
        'buff': [
            ('E', 0, 10),
            ('W', 5, '1'),
            ('W', 7, '1'),
        ],
        'optimized': [
            ('E', 0, 5),
            ('W', 5, '1'),
            ('E', 6, 1),
            ('W', 7, '1'),
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
            ('W', 0, 'a'),
            ('W', 0, 'b'),
        ],
        'optimized': [
            ('W', 0, 'b'),
        ],
    },
    {
        'buff': [
            ('E', 0, 3),
            ('W', 4, 'a'),
            ('E', 0, 5),

        ],
        'optimized': [
            ('E', 0, 5),
        ],
    },
]

디폴트값 = '0x00000000'
캐시사이즈 = 100


def make_temp_cache(cmd) -> dict:
    cache_temp = {i: None for i in range(캐시사이즈)}
    for action_type, addr, c in cmd:
        if action_type == 'E':
            for i in range(addr, addr + c):
                cache_temp[i] = 디폴트값
        if action_type == 'W':
            cache_temp[addr] = c
    return cache_temp


@pytest.fixture
def controller():
    return SSDController()


def test_controller_buffer_optimize_method_is_exist(controller):
    assert hasattr(controller, 'buffer_optimize')


@pytest.mark.parametrize("buffcmd, optimized_cmd", [(i['buff'], i['optimized']) for i in cases])
def test_controller_buffer_try(controller, buffcmd, optimized_cmd):
    temp_cache = make_temp_cache(buffcmd)
    assert controller._generate_commands(temp_cache, buffcmd) ==optimized_cmd


