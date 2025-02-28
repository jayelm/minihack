#!/usr/bin/env python
#
# Copyright (c) Facebook, Inc. and its affiliates.
import multiprocessing as mp

import gym
import pytest

import minihack  # noqa: F401

START_METHODS = [
    # TODO uncomment spawn after the next NLE release
    # m for m in ("fork", "spawn") if m in mp.get_all_start_methods()
    m
    for m in ("fork")
    if m in mp.get_all_start_methods()
]


def new_env_one_step():
    env = gym.make("MiniHack-Room-15x15-v0")
    env.reset()
    obs, reward, done, _ = env.step(0)
    return done


@pytest.mark.parametrize(
    "ctx", [mp.get_context(m) for m in START_METHODS], ids=START_METHODS
)
class TestEnvSubprocess:
    def test_env_in_subprocess(self, ctx):
        p = ctx.Process(target=new_env_one_step)
        p.start()
        p.join()
        assert p.exitcode == 0

    def test_env_before_and_in_subprocess(self, ctx):
        new_env_one_step()
        p = ctx.Process(target=new_env_one_step)
        p.start()
        p.join()
        assert p.exitcode == 0
