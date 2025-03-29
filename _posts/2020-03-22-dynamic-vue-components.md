---
title: Dynamically Loading Vue Components by Route
date: '2020-03-22T23:46:37.121Z'
layout: post
tags: archive
---

When I decided to create this blog with Vue, I found
[this post by @vycoder](https://dev.to/vycoder/creating-a-simple-blog-using-vue-with-markdown-2omd) to be very helpful in
helping me decide how to structure the site. I liked the idea of writing
my blog posts with Markdown and then using a Webpack Markdown loader to
allow me to render the posts inside of Vue components. The idea is to use
Webpack's <code>import</code> function to dynamically associate a list of
Markdown files with specific routes using Vue Router.

For my blog, I ended up just using regular Vue files to write my posts since this was the easiest way I could find to render syntax highlighted code blocks. However, the idea still works the same way in practice - use the URL to determine which file to dynamically load and render.

If you read the post, you'll notice that the author dynamically loads his Markdown files directly into his Vue Router. This means that the contents of each loaded blog post would be rendered wherever the <code>\<router-link /></code> component exists inside of your App.vue file (if you used the Vue CLI to create your project).

Although this is a really cool concept, it wasn't quite powerful enough for what I wanted to do with my blog. What if I wanted to associate meta data such as tags or a date with each blog post, and then dynamically render each post inside of a wrapper component that would render the meta data however I wanted?

I'll explain what I mean by this. Here's a simple JSON file containing information about a couple of example blog posts:

```javascript
[
  {
    "slug": "first_post",
    "title": "My first blog post",
    "tags": ["blog", "cool"],
    "description", "Come read my first blog post"
  },
  {
    "slug": "second_post",
    "title": "My second blog post",
    "tags": ["awesome", "cool"],
    "description": "A follow up to my first post"
  }
]
```

I wanted to be able to take the tags from each blog post and render it in a wrapper component around the actual post data. So instead of mapping each individual loaded Markdown file to its own route, I wanted a single route that could take the post's slug and use that to dynamically load the post and its information using the meta JSON file. I started out with a Vue router file looking something like this:

```javascript
import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/posts/:slug',
    name: 'BlogPost',
    component: () => import('@/views/BlogPost.vue'),
    props: true,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
```

Notice that the <code>/posts</code> route has a URL param called slug, which will then be passed as a prop to the <code>BlogPost.vue</code> component. Our <code>BlogPost</code> component can then use the slug passed to it to look up meta data in our JSON file and then dynamically load the Vue file with the slug's name.

This is the <code>BlogPost</code> component I started out with:

```html
<template>
  <div>
    <h1>{{ title }}</h1>
    <ul>
      <li v-for="(tag, idx) in tags" :key="idx">{{ tag }}</li>
    </ul>
    <component :is="postComponent" />
  </div>
</template>

<script>
  import postsMeta from '@/posts/meta.json';

  export default {
    props: {
      slug: {
        type: String,
        required: true,
      },
    },
    data: () => ({
      title: '',
      tags: [],
      postComponent: null,
    }),
    async created() {
      try {
        this.title = postsMeta[this.slug].title;
        this.tags = [...postsMeta[this.slug].tags];
        this.postComponent = (
          await import(`@/posts/${this.slug}/index.vue`)
        ).default;
      } catch (err) {
        this.$router.push('/400');
      }
    },
  };
</script>
```

The real power is in the created hook. The slug prop is passed in via the URL. It is then used to insert the title and tags associated with the post into data members. So if I navigate to <code>/posts/first_post</code>, the title "My first post" and the tags "blog" and "cool" will be available in our data members.

This line is where the component is dynamically loaded:

```javascript
this.postComponent = (await import(`@/posts/${this.slug}/index.vue`)).default;
```

I created a folder inside of my <code>posts</code> folder with the same name as the slug, and then placed an <code>index.vue</code> file inside with the content. Since the <code>import</code> function is asynchronous, we must wait on it. Since we are loading an ES6 module, we must use the <code>default</code> property of the result to get the actual component. Now the post is loaded into the <code>postComponent</code> data member.

Finally, the component is loaded into the <code>BlogPost</code> container in this line in the template:

```html
<component :is="postComponent" />
```

You'll also notice that the title is placed inside of an <code>h1</code> tag and that the tags are placed inside of an unordered list. Of course, this is just a simple example for what you could do to render your meta data - add however much CSS you want to make it look good.

And that's all you need! I'm constantly amazed by the power you can achieve with Vue with such a simple syntax. I've heard it said that there really is no such thing as "advanced" Vue because it's all so easy to use. There are only new things to learn - so go out and see what cool projects you can build with the power of dynamic components!
