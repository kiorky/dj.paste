================
afpy.trac package
================

.. contents::

What is dj.paste
==================

It is just another wsgi wrappers:

    * one for django
    * one for getting an app factory for werkzeug's DebuggedApplication

How to use dj.paste
=====================


Django App
----------------
With paste, just add another app entry with a django_settings_module  variable to point to
your django settings ::

    [composite:main]
    use = egg:Paste#urlmap
    / = foo

    [app:foo]
    egg=afpy.trac
    django_settings=foo.settings

DebuggedApplication App
------------------------
With paste, just add another app entry with a django_settings_module  variable to point to
your django settings ::

    [DEFAULT]
    debug=true
    [composite:main]
    use = egg:Paste#urlmap
    / = p
    [pipeline:p]
    pipeline =  exc
                foo

    [app:foo]
    egg=afpy.trac
    django_settings=foo.settings

    [filer:exc]
    use=egg:dj.paste#debug

