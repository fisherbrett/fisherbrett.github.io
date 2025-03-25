---
title: Introducing My New Next.js Blog (with a free template you can use for your own blog!)
date: 2024-09-23
layout: post
---

Ever since I started working full time, I haven't had much time to work on my blog. I've been wanting to update it for a while now, and I finally got around to it. The last version of my blog was made with Gatsby, and while I loved it, I wanted to try something new. I decided to remake my blog with Next.js and Tailwind CSS. Here's how I did it.

(If you'd like to create your own blog and skip the setup, you can use this template I created: [https://github.com/bandrewfisher/next-js-markdown-blog-template](https://github.com/bandrewfisher/next-js-markdown-blog-template))

## Creating the project

I followed the instructions on the [Next.js website](https://nextjs.org/docs/getting-started/installation) to create a new project. All I had to do was run this command, and then follow the prompts:

```bash
npx create-next-app@latest
```

The project it creates comes with Tailwind CSS and TypeScript already set up, which is a big time saver.

## Setting up Contentlayer

I wanted to be able to write my blog posts in Markdown, so I decided to use [Contentlayer](https://contentlayer.dev/). Contentlayer is a tool that lets you load content from Markdown files into your Next.js project. It's super easy to set up, and it works great with Tailwind CSS. Plus, you can take advantage of Next.js's static site generation to make your blog super fast and SEO-friendly.

I followed the instructions on the [Contentlayer website](https://contentlayer.dev/docs/getting-started-cddd76b7) to set it up. 

First, I installed the Contentlayer dependencies:

```bash
npm install contentlayer next-contentlayer date-fns rehype-prism-plus
```

We'll use the [`rehype-prism-plus`](https://github.com/timlrx/rehype-prism-plus) package later to add syntax highlighting to our blog posts.

Then, I updated my `next.config.mjs` file to use Contentlayer:

```javascript
// next.config.mjs
import { withContentlayer } from "next-contentlayer";

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  ...
};

export default withContentlayer(nextConfig);
```

I updated my `tsconfig.json` to add an import alias and include the generated Contentlayer files:

```javascript
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      ...
      "contentlayer/generated": ["./.contentlayer/generated"]
    },
    ...
  },
  "include": [
    ...
    ".contentlayer/generated"
  ]
}
```

I added `.contentlayer` to my `.gitignore` file:

```
# .gitignore
.contentlayer
```

Then, I added a `contentlayer.config.js` file to define the schema for our blog posts:

```javascript
// contentlayer.config.js
import { defineDocumentType, makeSource } from "contentlayer/source-files";
import rehypePrism from "rehype-prism-plus";

export const Post = defineDocumentType(() => ({
  name: "Post",
  filePathPattern: `**/*.md`,
  fields: {
    title: {
      type: "string",
      required: true,
    },
    date: {
      type: "date",
      required: true,
    },
    description: {
      type: "string",
      required: true,
    },
  },
  computedFields: {
    url: {
      type: "string",
      resolve: (post) => `/posts/${post._raw.flattenedPath}`,
    },
  },
}));

export default makeSource({
  contentDirPath: "posts",
  documentTypes: [Post],
  markdown: { rehypePlugins: [rehypePrism] },
});
```

[rehypePrims](https://github.com/timlrx/rehype-prism-plus) is a plugin for syntax highlighting in Markdown files with [Prism](https://prismjs.com/). We'll come back to that later.

This config file tells Contentlayer to look for Markdown files in the `posts` directory and create a `Post` document type with `title`, `date`, and `description` fields. It also tells Contentlayer to generate a `url`