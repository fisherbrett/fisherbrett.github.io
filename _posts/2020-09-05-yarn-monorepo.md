---
title: How to Create A Monorepo with Yarn Workspaces
date: '2020-09-05T23:46:37.121Z'
layout: post
---

TLDR; If you'd prefer to just see the working code, view the whole project here: https://github.com/bandrewfisher/monorepo-tutorial

For the past couple of years, I've been working on a project for a professor at my university. It's a site that facilities research in ancient Assyrian trade. It's been a ton of fun and I've learned so much about web development in the process. For a while, I've maintained three separate Git repositories for the project - one for the Vue frontend, one of the TS Express backend, and a third one containing utility code shared between the other two repositories.

This was tricky to maintain, to say the least. The codebase is relatively small, so I figured it would be more maintainable to move everything to a single repository. In this post I'll explain how you can easily create a monorepo for JS projects with multiple packages.

## Create a Project

Create a new directory and then initialize it with Yarn:

```bash
$ mkdir vue-express-monorepo
$ cd vue-express-monorepo
$ yarn init -y
```

## Setup Yarn Workspaces

To create a monorepo, we will use [Yarn workspaces](https://classic.yarnpkg.com/en/docs/workspaces/). According to the docs, this "allows you to setup multiple packages in such a way that you only need to run `yarn install` once to install all of them in a single pass." If you are using npm, then there's a pretty good tool called [Lerna](https://lerna.js.org/) that can help you accomplish the same goal. [Yarn workspaces don't claim to replace Lerna](https://classic.yarnpkg.com/en/docs/workspaces/#toc-how-does-it-compare-to-lerna), but for my purposes I've found that so far I've been able to use Yarn workspaces without Lerna.

We will create two packages and put them inside a directory called `packages`. Create a `packages` directory:

```bash
$ mkdir packages
```

We need to tell Yarn that the `packages` directory contains our packages. Edit your `package.json` file so that it looks like the following:

```js
{
  "name": "vue-express-monorepo",
  "private": true,
  "workspaces": [
    "packages/*"
  ]
}
```

Now we're ready to create our packages.

## Create Packages

Create a directory in the `packages` directory. Initialize it with Yarn and create an `index.js` file:

```bash
$ cd packages
$ mkdir package-a
$ cd package-a
$ yarn init -y
$ touch index.js
```

Now add this to your `index.js` file:

```js
function packageAFunc() {
  console.log('Using a function from package A');
}

module.exports = packageAFunc;
```

Let's create another package and then use this function from `package-a` inside of it.

```bash
$ cd ..
$ mkdir package-b
$ cd package-b
$ yarn init -y
$ touch index.js
```

Add the following to your `index.js` file in `package-b`:

```js
const packageAFunc = require('package-a');

packageAFunc();
```

Finally, you just need to run a `yarn install` in the root level of your project.

```bash
$ cd ../..
$ yarn install
```

Yarn will link `package-a` and `package-b` in a `node_modules` folder in the project root.

Try running the `package-b` file:

```bash
$ node packages/package-b/index.js
```

You should see "Using a function from package A" printed to the console!

## Conclusion

Converting the site I've been building to use a monorepo has been incredibly helpful. This is a super simple example, but I used the same concepts from this post to create a monorepo with three separate frontend, backend, and utility packages. This has made sharing code throughout the project much easier. It's really nice that Yarn comes with this interesting feature that makes creating a monorepo so easy.

One of the main advantages I've noticed of this approach has been continuous deployment for the site. With everything living in one repository, it was easy to write a build script that built my Vue frontend and TS Express backend before deploying it all to AWS. I think this would have been a bit trickier if the site was still spread across multiple repositories.

I posted the link to my GitHub repo with the complete code, but here it is again for good measure: https://github.com/bandrewfisher/monorepo-tutorial
