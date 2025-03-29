---
title: Why I Converted from Vue to React
date: '2020-07-03T23:46:37.121Z'
layout: post
tags: archive
---

**EDIT: After receiving a lot of comments on this post, I realized that not all of the information I presented is accurate. I just released an updated version of this article that you can read [here](/posts/why-i-switched-to-react-new/). I will keep this article for historical reasons, but note that I don't hold all of the same views that I have presented here.**

I've been a long time VueJS fan and still think it's a great framework with a lot of potential.
It was the first JS framework I learned and will always have a special place in my heart.
In fact, when I first started learning React, I was convinced that I would never leave Vue.
It's easy to learn and with the Vue CLI, you can create a functional site in minutes and easily deploy
it with something like Netlify (which is what I use for my blog). I liked the organization of the `.vue`
files with their separate HTML, JS, and CSS sections. When I got a job as a React developer, I
found it easy to get confused by React files since the logic for rendering JSX could easily get
out of hand. I missed Vue files where if I wanted to know what the DOM would look like, I just
had to scroll to the top of the file and I would see everything HTML related.

I've been working professionally with React for about 7 months now, and in that time I've gradually
seen the beauty of React and have decided that it will from now on be my JS framework of choice
(at least, until it's outdated and something even better comes along! Welcome to the front-end world...).
I even decided to rewrite this blog with React, having originally created it with Vue.
I'd like to explain a few reasons why React won me over.

## 1. There's no magic in React

One of the things I love most about React is that it is literally just JavaScript. To create a React component,
all I have to do is write a regular JavaScript function that happens to return JSX. That's it, it just works!
The way I think of it, JSX is basically the one thing that sets a functional React component apart
from a normal JS function. Even React hooks are just functions - yes, you would only use them for
React, but at the end of the day they're just functions. There's really nothing magical about them.

Since React is just JavaScript, I don't have to guess at all about where the code that's being used is coming from.
Compare that to Vue where you have these "magic" functions and directives like `$emit` or `v-for`. In React,
I don't have to "emit" an event. I just pass a callback function. That's pure JS, no magic there. In React,
I don't need to remember some React specific directive to render a list of objects - I just use the JS `map`
function and return JSX.

Let's take the following as an example: a component that renders a list of users with a button allowing you
to follow that user. Maybe we could use this in a social media app. Here's the Vue version:

```html
<!-- UserComponent.vue -->
<template>
  <ul>
    <li v-for="user in users" :key="user.id">
      {{ user.name }}
      <button @click="$emit('followUser', user.id)">Follow</button>
    </li>
  </ul>
</template>

<script>
  export default {
    data: () => ({
      users: [
        {
          id: 1,
          name: 'Rick',
        },
        {
          id: 2,
          name: 'Morty',
        },
        {
          id: 3,
          name: 'Summer',
        },
      ],
    }),
  };
</script>
```

Pretty simple, right? We have a list of `users` that we render along with
a button next to each of the user's names. When clicking the follow button,
a `followUser` event is emitted along with the ID of the user we followed.

Here's the same idea with React:

```jsx
// UserComponent.jsx

import React from 'react';

const users = [
  {
    id: 1,
    name: 'Rick',
  },
  {
    id: 2,
    name: 'Morty',
  },
  {
    id: 3,
    name: 'Summer',
  },
];

export default function ({ onFollowUser }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          {user.name}
          <button onClick={() => onFollowUser(user.id)}>Follow</button>
        </li>
      ))}
    </ul>
  );
}
```

The beauty I find in the React implementation is what I was saying before -
this is just JavaScript that happens to be able to return HTML. If I were a new
developer, as long as I knew regular JS I would be able to look at the React version
and basically know what was going on.

If I were a new Vue developer looking at the
Vue version, I'd have to know what `v-for` is and where on earth `$emit` is coming
from. I would also probably want to know more about that `data` property in the default
export of the Vue file. Those are all things I'd have to go learn from the Vue docs. Of course,
there's nothing wrong with that - to master the tools you use as a developer, you must
be familiar with the docs. But when I was a Vue developer, I had those docs open every
single day. As a React developer, I occassionally look at the Hooks API reference in the
React docs when I'm fuzzy on what one of the hooks does. Other than that, I don't _need_
to look at the React docs because I'm just writing JavaScript.

## 2. React has better TypeScript support

As I described in [my last blog post](/typescript-template/), I've recently become quite fond of TypeScript.
One of the things I love most about TypeScript is the Intellisense you get from your IDE when developing.
When dealing with dynamic objects such as network or database responses, your editor can't give you
any kinds of hints as to what kinds of properties exist on those objects when you're using regular old
JavaScript. With TypeScript, however, all you have to do is define a type for such responses, and
all of the sudden it's so much easier to manipulate those data since your editor knows what properties
you're dealing with. No more accidentally spelling a property name wrong and then wondering why your
code is crashing!

The internet is already saturated with articles containing long praises for TypeScript, so I'll stop myself
there. At the end of the day, TypeScript scales _far_ better than regular JavaScript, and I've found
that React plays a lot nicer with TypeScript than Vue does.

A big part of the reason goes back to the fact that React is pretty much just JavaScript while
Vue kind of lives in its own little world. Creating a TypeScript React app is as easy as running
`npx create-react-app my-app --template typescript`, and everything just works.

Now, the Vue CLI also lets you create a TypeScript project. Just run `vue create my-project-name`,
and then you can choose to create a TypeScript project. There are a couple of problems with this, though. As explained in the [Vue composition API RFC](https://composition-api.vuejs.org/#better-type-inference),
the only way to really make Vue play nicely with TS is by using [class component decorators](https://github.com/vuejs/vue-class-component),
which I am not a fan of. I used TS with the Vue class component decorators for a class project,
and I felt like it was hard to find good documentation and that there just wasn't a big enough
community using Vue this way such that I could easily find online answers to what I thought would be common
problems.

For another project, I actually decided to use the experimental [Vue composition API plugin](https://github.com/vuejs/composition-api),
which meant I didn't have to use the class components I despised and could still enjoy pretty nice TS support.
[Technically it's not recommended to use this plugin in production code](https://composition-api.vuejs.org/#adoption-strategy), but I did
anyways because I _really_ didn't want to use class components. Also, the project where I used it will only ever be heavily
used by a handful of ancient Assyrian researchers, so I wasn't too concerned about massive scalability.

The nice thing is, the composition API will be available by default in Vue 3, so I will give Vue credit for
improving its TS support. For me, though, what makes React win the battle is the Intellisense available in the JSX.
Vue still has its template section at the top, and even with TS, there isn't a great way for your editor to error check it.
On the other hand, linters with React + TS
will work just fine with JSX since you're just writing JavaScript inside.

Let's create a simple counter app in Vue and React using TypeScript as an example. Both apps
will contain a typo. Here's the Vue version (using the composition API plugin):

```html
<template>
  <div>
    <!-- Typo! But ESLint has no idea! -->
    <button @click="increaseCouter">Click me</button>
    You've clicked the counter {{ counter }} times
  <div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from "@vue/composition-api";

export default defineComponent({
  name: "CounterApp",
  setup() {
    const counter: Ref<number> = ref(0);

    const increaseCounter = (): void => {
      counter.value += 1;
    }

    return {
      counter,
      increaseCounter
    };
  }
});
</script>
```

Here's the same app in React:

```jsx
import React, { useState } from 'react';

const CounterApp = () => {
  const [counter, setCounter] = useState(0);

  const increaseCounter = (): void => {
    setCounter(prevCounter => prevCounter + 1);
  };

  return (
    <div>
      {/* Typo! But this time, ESLint spots it for us! */}
      <button onClick={increaseCouter}>Click me</button>
      You've clicked the counter {counter} times
    </div>
  );
};

export default CounterApp;
```

In both of the apps, "increaseCounter" is misspelled "increaseCouter". You can set up ESLint
in both projects no problem, but it's not going to catch the typo in the Vue project. You'll
be just fine in the React project since React is just JavaScript and ESLint will immediately
recognize that "increaseCouter" is not defined.

Now, to Vue's credit, it does give pretty good error messages, so for this example when you run
your app you will get an error about "increaseCouter" being undefined. However, you may not
always get such instant feedback once you start dealing with more complicated code.
Of course, just using TypeScript in React is not a guarantee that your code will be bug free.
But you can automate error catching silly mistakes like the one above much easier than with Vue.

With some configuration, there actually [is a way to use JSX with Vue](https://vuejs.org/v2/guide/render-function.html#JSX),
so that could solve this problem. But at the moment, there doesn't seem to be a big community
doing this, so you might have a hard time finding answers when you run into problems. At that point,
you might as well just be using React which supports JSX out of the box.

## 3. React is easier to test

Back when I worked as Vue developer, I began learning about the importance of test driven development.
It took me quite a while to get used to the mindset of writing my tests at the same
time that I wrote my application code, but now I'm at the point where I feel like
I can't live without a decent test suite even for small side projects.

I began developing this mindset around the same time that I began to embrace TypeScript.
I found quite difficult to test my Vue components, even when I got
them working with TypeScript. While using the Vue composition API plugin, I found
that [Vue Test Utils](https://vue-test-utils.vuejs.org/) a lot of the times weren't
able to correctly render the components I was creating. This probably shouldn't have
come as a surprise to me. I doubt the team maintaining Vue Test Utils was too focused
on getting tests to work with the composition API plugin when the composition API is going
to ship natively with Vue 3 anyways.

Vue Test Utils is actually pretty decent when you're using Vue 2's options API
with regular JavaScript. Once I started using Vuetify though,
which is a fantastic library, I immediately began running into problems. Getting
the Vue test utils to recognize the Vuetify components was a bit of a pain
and I don't think I ever really figured out how to get tests working properly with Vue + Vuetify
or Vue + TypeScript. Maybe there's something I was missing. If so, I'd love to learn
about it.

With React, I've never really run into super weird errors when trying to set up unit
testing, even when using TypeScript or a component library like [Material UI](https://material-ui.com/).
Once again, this all basically goes back to the fact that React is just JavaScript.
There's no magic - all of its dependencies are `import`ed in each file, which
makes mocking them with Jest trivial. With something like Vuetify, all the components
are kind of "magically" available, which is why I was running into so many problems
trying to test them. Now, I know that shallow rendering the components would have solved
those problems easily, but I agree with Kent C. Dodds that [shallow rendering components
doesn't really get them tested the way they should be](https://kentcdodds.com/blog/why-i-never-use-shallow-rendering).

## Conclusion

The purpose of this post was not to say that Vue is bad - in fact, during the year and a
half time span that I worked professionally with Vue, for the most part I was quite pleased with it
and still believe it to be a fantastic frontend framework. I think that it is an easy framework
to learn and a good starting place for new web developers. I developed the reasons I have
for switching to React as a result of my own experiences. As I mentioned,
TypeScript is almost a must have for me, and I find it a lot easier to use with React
than Vue. But for someone who doesn't necessarily want to use TypeScript, React
may not provide such a clear advantage over Vue.

I'll also readily admit that some of the problems I mentioned with Vue almost certainly
have solutions that I am not aware of, and I'm willing to learn about them! In my own
experience, I just found it a lot easier to solve the problems I was facing with
React than Vue. At the end of the day, this post really just represents my own
opinion and is shaped by what I consider important as a web developer.
Someone with a different set of experiences may prefer Vue, and that's totally fine.
But for now, I'll be sticking with React.
