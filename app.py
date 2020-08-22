#!/usr/bin/env python3

from aws_cdk import core

from ab3.ab3_stack import Ab3Stack


app = core.App()
Ab3Stack(app, "ab3")

app.synth()
