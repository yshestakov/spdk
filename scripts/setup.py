#!/usr/bin/env python

from distutils.core import setup

long_description = 'Storage Performance Development Kit'

setup(
    name='spdk-rpc',
    version='20.01',
    author='SPDK Mailing List',
    author_email='spdk@lists.01.org',
    description='SPDK RPC modules',
    long_description=long_description,
    url='https://spdk.io/',
    packages=['rpc', 'spdkcli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['spdk_rpc.py', 'spdkcli.py'],
    data_files=[
        ('/usr/share/spdk_rpc',
            ['config_converter.py', 'dpdk_mem_info.py',
             'histogram.py', 'iostat.py', 'rpc_http_proxy.py']
            )
        ]
)
