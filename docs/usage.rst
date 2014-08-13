=====
Usage
=====

Basic
-----

Since this is a common flask-application, after installation, you can immediately run it as usual.

.. code-block:: bash

    uwsgi -s /tmp/uwsgi.sock -w nidhogg.run:app

Or, run in debug mode:

.. literalinclude:: ../nidhogg/run.py

Advanced
--------
If you want to use **flask-nidhogg*** in a project:

.. code-block:: python

    import nidhogg

…and do what you want — add blueprint into your Flask project, use objects for validation, create responces, etc.
