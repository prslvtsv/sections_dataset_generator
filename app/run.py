# -*- coding: utf-8 -*-
"""
24 Jun 2022

@author: prslvtsv

"""
import os
import sys
ROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from textual.app import app
from textual.widgets import Placeholder

#fmt: off
class TilingSolvingApp(App):
    async def on_mount(self):
        await self.view.dock(Placeholder(). edge="left", size=40)
