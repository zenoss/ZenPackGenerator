==============================================================================
Usage
==============================================================================

Basic usage information can be generated from the Generators help mechanism.

* zpg -h

The most basic usage will involve creating a json input and then specifying a destination
prefix for the ZenPack.

* zpg :doc:`input.json <jsonformat>` /tmp/output

Best practices indicate moving the input.json file into /tmp/output/*<ZenPack>* once you have run the generator.  You may wish to use the json again to regenerate the ZenPack.

Making Changes
--------------
Oftentimes a zenpack will require additional code to fully function.  It is possible to make changes to the source templates and regenerate the zenpack so that it will include the additional code in your files.

You can modify the `Source Templates <http://cheetahtemplate.org>`_ found at
/tmp/output/*<ZenPack>*/Templates, and rerun the generator for the changes to take effect.

If you discover that you are missing a Component, or need to add an additional property to a component.  You can just add that information to the json file and rerun the generator and the required files will be automatically updated.

.. warning::

    However, there is a significant limitation to this regenerative process.  Currently the Generator cannot determine if a Component has been removed or renamed.  You will have to resolve those inconsistancies by hand if you choose to do this.

