#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scrapy.cmdline import execute

if __name__ == "__main__":
    name = "jiang_xi_drug"
    cmd = f"scrapy crawl {name}"
    execute(cmd.split())
