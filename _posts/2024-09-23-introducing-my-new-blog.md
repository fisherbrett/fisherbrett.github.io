---
title: Introducing My New Next.js Blog (with a free template you can use for your own blog!)
date: 2024-09-23
description: I remade my blog with Next.js and Tailwind CSS. Here's how I did it.
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

This config file tells Contentlayer to look for Markdown files in the `posts` directory and create a `Post` document type with `title`, `date`, and `description` fields. It also tells Contentlayer to generate a `url` field for each post that we can use to link to the post.

I created a few Markdown files (.md extension) in the `posts` directory to test it out.

They would look something like this:

```
---
title: My new blog
date: 2024-09-23
description: Something about the post
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit...
```

### Rendering the blog posts

Right now, we have Contentlayer set up to generate HTML content for our Markdown blog posts, but we need a way to render that content in our Next.js app. We can do this by creating a new page in our `pages` directory that uses the `generateStaticParams` function to generate static paths for each one of our posts.

I created a new file called `[slug].tsx` in the `pages/posts` directory:

```javascript
import { format, parseISO } from "date-fns";
import { allPosts } from "contentlayer/generated";

export const generateStaticParams = async () =>
  allPosts.map((post) => ({ slug: post._raw.flattenedPath }));

export const generateMetadata = ({ params }: { params: { slug: string } }) => {
  const post = allPosts.find((post) => post._raw.flattenedPath === params.slug);
  if (!post) throw new Error(`Post not found for slug: ${params.slug}`);
  return { title: post.title };
};

const PostLayout = ({ params }: { params: { slug: string } }) => {
  const post = allPosts.find((post) => post._raw.flattenedPath === params.slug);
  if (!post) throw new Error(`Post not found for slug: ${params.slug}`);

  return (
    <article className="prose mx-auto max-w-xl py-8">
      <div className="mb-8 text-center">
        <time dateTime={post.date} className="mb-1 text-xs text-gray-600">
          {format(parseISO(post.date), "LLLL d, yyyy")}
        </time>
        <h1 className="text-3xl font-bold">{post.title}</h1>
      </div>
      <div
        className="[&>*]:mb-3 [&>*:last-child]:mb-0"
        dangerouslySetInnerHTML={{ __html: post.body.html }}
      />
    </article>
  );
};

export default PostLayout;
```

Now, each post will have its own page with a URL like `/posts/my-new-blog`. The `generateStaticParams` function generates the static paths for each post, and the `generateMetadata` function generates the metadata for each post, which we can use to set the page title.

If you wrote a post called `my-new-blog.md`, you would be able to access it at `http://localhost:3000/posts/my-new-blog`.

However, since Tailwind removes all default styling for HTML elements, you'll probably notice that the blog post doesn't look very good. If you added headers, for example, they'll look the same as regular text.

That's what the `prose` class is for, even though it won't do anything now. This comes from the Tailwind CSS Typography plugin, which provides a set of typographic defaults that will make our blog content look beautiful. Let's set it up.

## Setting up Tailwind CSS Typography

Install the plugin from the instructions given in the [GitHub repository](https://github.com/tailwindlabs/tailwindcss-typography):

```bash
npm install -D @tailwindcss/typography
```

Now add the plugin to your `tailwind.config.js` file:

```javascript
// tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    // ...
  },
  plugins: [
    require("@tailwindcss/typography"),
    // ...
  ],
};
```

And that's it! Now your blog posts will look much better.

## Syntax highlighting

Remember the `rehypePrism` plugin we added to our Contentlayer config? Now we can use it to add syntax highlighting to our blog posts.

First, install the Prism CSS theme you want to use. You can find a list of themes on the [Prism website](https://prismjs.com/). I'm just going to use the default theme and select a few languages I want to highlight, like Python, JavaScript, and bash.

Download the CSS file and add it to `app/prism.css`.

Now in my `app/layout.tsx` file, I added this line:

```javascript
// app/layout.tsx
import "./prism.css";
```

Add a code block to your Markdown post:

```python
def hello_world():
    print("Hello, world!")
```

And that's it! Now your code blocks will have syntax highlighting. It works because of the `rehypePrism` plugin we added to our Contentlayer config. It will split up the code blocks in your Markdown files and add the necessary classes for Prism to highlight them.

## Displaying all of our blog posts

Right now we can navigate directly to our posts, but we have no way to see all of them at once. Let's create a new page that lists all of our blog posts.

I created a new file called `page.tsx` in the `pages/posts` directory:

```javascript
import Link from "next/link";
import { compareDesc, format, parseISO } from "date-fns";
import { allPosts, Post } from "contentlayer/generated";

function PostCard(post: Post) {
  return (
    <div className="mb-8">
      <h2 className="mb-1 text-xl">
        <Link
          href={post.url}
          className="text-blue-800 hover:underline hover:underline-offset-2"
        >
          {post.title}
        </Link>
      </h2>
      <time dateTime={post.date} className="mb-2 block text-xs text-gray-600">
        {format(parseISO(post.date), "LLLL d, yyyy")}
      </time>
      <div className="text-sm [&>*]:mb-3 [&>*:last-child]:mb-0">
        {post.description}
      </div>
    </div>
  );
}

export default function Blog() {
  const posts = allPosts.sort((a, b) =>
    compareDesc(new Date(a.date), new Date(b.date))
  );

  return (
    <div className="mx-auto max-w-xl">
      <h1 className="mb-8 text-center text-3xl font-black">Blog</h1>
      {posts.map((post, idx) => (
        <PostCard key={idx} {...post} />
      ))}
    </div>
  );
}
```

This will display all of the blog posts in reverse chronological order. Each post will have a title, date, and description, and you can click on the title to navigate to the post.

You can access this page at `http://localhost:3000/posts`.

## Conclusion

That's it! We've set up a new blog with Next.js, Tailwind CSS, and Contentlayer. We've created a way to write blog posts in Markdown, render them in our Next.js app, and display them on a blog page. We've also added syntax highlighting to our code blocks and made our blog posts look beautiful with Tailwind CSS Typography.

## Use this template for your own blog!

That was a lot of work, but you don't have to do it all yourself. I created a [GitHub repository](https://github.com/bandrewfisher/next-js-markdown-blog-template) with all of this setup work already done for you. Just clone it and run `yarn install` and then `yarn dev` to get started. You can use it as a starting point for your own blog and customize it however you like.
