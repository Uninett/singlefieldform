========================================
Single field forms: a pattern experiment
========================================

This is a tiny Django site that shows what you can do with forms with only
a single field, subclassing and HTMx.

Depends only on Django 5.2+.

Usage
=====

1. Put the cide somewhere and stand in the same directory as this file
2. Get a virtual env your preferred way, for instance::

   $ python3 -m venv .venv && source .venv/bin/activate
3. Install the package in the venv::

   $ pip install -e .
4. Create the sqlite database::

   $ python manage.py makemigrations
4. Run the demo::

   $ python3 manage.py runserver
5. Visit the demo at `http://127.0.0.1 <http://127.0.0.1>`_
