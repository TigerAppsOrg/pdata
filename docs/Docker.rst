Docker
======

General Guidelines
------------------

1. It is preferable to place heavy (time-consuming or resource-intensive) build
   steps earlier in the Dockerfile. Similarly, steps that frequently change
   should be placed towards the end of the Dockerfile.
   Build steps are executed sequentially, but they are also cached in this
   order. Any time a build step's cache is invalidated, all of the subsequent
   steps are also invalidated. Therefore, placing heavy steps first and
   frequently-changing steps last maximizes the caching possible.

2. Minimize build artifacts by deleting extraneous artifacts when no longer
   needed. This reduces the image size which is beneficial for numerous
   reasons, including the amount of time it takes to deploy a new image.

   One way to accomplish this is to delete build dependencies in :code:`apk`
   as part of the build step itself.
