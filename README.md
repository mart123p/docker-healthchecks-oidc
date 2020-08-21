# Healthchecks Docker

This container is a fork of [linuxserver.io](https://github.com/healthchecks/healthchecks) docker container to add the OpenID Connect support for the app. The provider is designed to use Microsoft Azure AD as a provider for OpenID Connect.

## Permissions

By default, a user needs to give access to individual teammates to a project where he is an 
owner. In this version, every project created is made public to the entire organization.

## Credits
Some of the code was inspired by the following issues in the healthchecks project.
- https://github.com/healthchecks/healthchecks/issues/299
- https://github.com/healthchecks/healthchecks/issues/185
