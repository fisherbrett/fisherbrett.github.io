---
title: How to Install a Specific Version of an NPM Package
date: '2020-09-21T23:46:37.121Z'
layout: post
---

The other day I got a warning in a Vue project I've been working on for a while. It was complaining about me using an unsupported version of TypeScript. I decided to download a supported version, but how was I supposed to do that?

First I uninstalled my existing version of TypeScript:

```bash
$ yarn remove typescript
```

Then after some quick Googling, I found this for downloading a specific NPM package version:

```bash
$ yarn add typescript@3.5.3
```

You can do the same thing with NPM:

```bash
$ npm install typescript@3.5.3
```

And that's it! You can do this for any NPM package:

```bash
$ yarn add some-package@version
// or
$ npm install some-package@version
```
