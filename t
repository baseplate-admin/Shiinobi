(shiinobi-project-py3.12) PS C:\Programming\Shiinobi> python .\test.py
Traceback (most recent call last):
  File "C:\Programming\Shiinobi\test.py", line 1, in <module>
    from shiinobi.builder.staff import StaffBuilder
  File "C:\Programming\Shiinobi\shiinobi\builder\staff.py", line 5, in <module>
    from shiinobi.utilities.session import session
  File "C:\Programming\Shiinobi\shiinobi\utilities\session.py", line 49, in <module>
    session = CachedLimiterSession(
              ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Programming\Shiinobi\shiinobi\utilities\session.py", line 21, in __init__
    super().__init__(*args, **kwargs)
  File "C:\Users\baseplate-admin\AppData\Local\pypoetry\Cache\virtualenvs\shiinobi-project-ldd4Q3aR-py3.12\Lib\site-packages\requests_cache\session.py", line 62, in __init__
    self.cache = init_backend(cache_name, backend, serializer=serializer, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\baseplate-admin\AppData\Local\pypoetry\Cache\virtualenvs\shiinobi-project-ldd4Q3aR-py3.12\Lib\site-packages\requests_cache\backends\__init__.py", line 88, in init_backend
    raise ValueError(
ValueError: Invalid backend: <pyrate_limiter.sqlite_bucket.sqlitebucket object at 0x000001571c61e930>. Provide a backend instance, or choose from one of the following aliases: ['dynamodb', 'filesystem', 'gridfs', 'memory', 'mongodb', 'redis', 'sqlite']