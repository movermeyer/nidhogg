=============
Configuration
=============


Before you do anything, you need to configure the application.
It's performed by two environment variables.

``NIDHOGG_SETTINGS_MODULE`` — main settings module (``'nidhogg.settings.base'`` by default)

``NIDHOGG_HASHER_MODULE`` — hasher module (``'nidhogg.common.hashers.generic'`` by default)

First variable points to the Flask config module with some additions.

.. literalinclude:: ../nidhogg/settings/base.py
    :lines: 8-

As you can see, this class describes table name for mapping and necessary column mames.
Be sure that you already create table for tokens and foreign key between this table ant users table.

.. literalinclude:: ../example.sql

Second variable is the hasher module, used for checking passwords with data from another table.
Interface for hasher module:

.. literalinclude:: ../nidhogg/common/hashers/generic.py

.. note::
    Flask-nidhogg distribution already shipped with standard WordPress passwords checker module.
    It will only work with CMS without plug-ins that change passwords hashing mechanism.
