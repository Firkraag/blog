#!/usr/bin/env python
# coding=utf-8

import os
WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(30) 
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '',
        'secret': ''
    },

    'twitter': {
        'id': '',
        'secret': ''
    },

    'github': {
        'id': '99f364dc1cd685976c1e',
        'secret': 'd322387d0906e8e18e0a007e699bfd55da763b14'
    }
}

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
