---
title: Why I Converted from Vue to React - UPDATED
date: '2020-07-25T23:46:37.121Z'
layout: post
tags: archive
---

[The original version of this article](/posts/why-i-switched-to-react/) got a lot more attention than I was expecting, especially since it was only my second post on dev.to. I'm grateful to everyone who read it and left feedback! As I read through the comments, I learned that some of the content of the original article wasn't entirely accurate and that I also wasn't clear about several of the points I was trying to make. My original article was an attempt to explain from a more technical standpoint why I chose React over Vue, but I realized I didn't quite have enough knowledge to tackle that in depth. In fact, I learned that I've gone the direction I have not because of "under the hood" differences between React and Vue, but instead out of small experiences that have shaped what feels the most comfortable for me in my career as a web developer. For other developers, Vue may feel more at home, and there's nothing wrong with that.

My intent was not and still is not to convince readers that React is inherently a better framework than Vue. Vue was the first web development framework I learned, and working with it was a delightful experience. I found its learning curve to be very forgiving compared to that of React. Ultimately, as I learned what was personally most important to me as a web developer, I decided to make the transition to use React as my front end framework of choice. I would still be happy to work with Vue professionally, but for personal projects, I believe that React better suits my needs. With that, I present a revised discussion on why I chose React over Vue.

## How I fell in love with Vue

I started learning how to code when I was about 16 years old. I started building simple console based programs in Perl before gaining intereset in web development. I got the first book I found at the library on web dev which taught me about PHP and jQuery, which I thought were amazing! I never did any major projects, but I enjoyed hacking up small apps in my free time.

Fast forward a few years to when I got my first web dev job. I was working for my university on their grade management site, and my job was to rewrite some of the existing front end pages to use Vue instead of [Backbone](https://backbonejs.org/) and/or PHP. Having only used jQuery, PHP, and sometimes even vanilla JS to create frontend pages, using Vue was definitely a different way of thinking for me. When I couldn't figure out how to do something with Vue, I would try using jQuery inside of my Vue components (which I quickly learned was a bad idea since jQuery manipulates the actual DOM, but Vue uses a [virtual DOM](https://vuejs.org/v2/guide/render-function.html#The-Virtual-DOM)).

However, after a lot of practice and making LOTS of mistakes, I embraced Vue and learned just how powerful it really is. I began using it for side projects and started attending a Vue Meetup hosted by a tech company close to where I live. I even ended up getting a summer internship at that company as a Vue + Rails developer. At a different job for my school, I chose to use Vue to create a fully functional site for the history department that they continue to use to research ancient Assyrian tablets.

Throughout these various jobs I had, I generally enjoyed working with Vue. It's known for its ease of use. One developer I worked with said that there isn't really such a thing as "advanced" Vue because it's all so easy to use (I slightly disagreed with him as I found things like [scoped slots](https://vuejs.org/v2/guide/components-slots.html#Scoped-Slots) and [render functions](https://vuejs.org/v2/guide/render-function.html) to take a little while to get used to, but I understand his point).

## My first taste of React

After I'd been working with Vue for almost a year, I signed up for a databases class where we were required to do a group project. Our team settled on using Python Flask for the backend and React for the frontend. I spent most of my time working on the backend, and once it was mostly complete, I offered to help with the frontend.

I hadn't worked with React before, and I began to understand why a lot of people said it was hard to learn. I learned enough to help out with our project, but I think it was mostly my lack of familiarity with React that didn't win me over at first. Hey, I was already familiar with Vue, so why should I abandon it when it had worked so well for me? I didn't see any advantage that switching to React would give me.

The next semester after I took that class, I decided to accept an internship with Bluehost as a React developer. Despite the title of this article, my first few months at the job working with React left a pretty bad taste in my mouth. I missed how concise Vue could be, and it drove me crazy that JSX could be thrown around almost anywhere in a React component. I began gaining a huge appreciation for Vue's single file components that had all the HTML in the `<template>` section of the file.

As a \*very\* simple example, this is the kind of code I would run into a lot at Bluehost ([see it on Codepen](https://codepen.io/brettfishy/pen/QWyYoWN)):

```jsx
import React, { useState } from 'react';

const UserDashboard = () => {
  const [view, setView] = React.useState('followers');
  const [user] = React.useState({
    name: 'John Doe',
    email: 'johndoe@example.com',
    followers: 1000,
    following: 500,
  });

  const renderProfile = () => {
    return (
      <ul>
        <li>Name: {user.name}</li>
        <li>Email: {user.email}</li>
      </ul>
    );
  };

  const renderFollowers = () => {
    return (
      <ul>
        <li>Followers: {user.followers}</li>
        <li>Following: {user.following}</li>
      </ul>
    );
  };

  return (
    <div>
      <section>
        <button onClick={() => setView('profile')}>Profile</button>
        <button onClick={() => setView('followers')}>Followers</button>
      </section>
      <section>
        {view === 'followers' ? renderFollowers() : renderProfile()}
      </section>
    </div>
  );
};
```

Of course a real app wouldn't have everything hardcoded like that, but it illustrates my point of the bewilderment I experienced upon seeing HTML treated like any other kind of object you can interact with in JavaScript. A lot of things about this way of coding made me an even stronger disciple of Vue, such as:

- Ternary operators used for rendering JSX just seemed...unnatural to me. I thought that Vue's `v-if` and `v-else` directives were much more intuitive.
- Having to declare dependencies for things like `useEffect` and `useCallback` seemed so primitive. I knew that ESLint plugins made it easy to find out which dependencies you might be missing, but there was no need to do anything like that in Vue's `methods` or `computed`.
- I most especially didn't like that JSX could appear anywhere in a React component. I had to work with some pretty big components at Bluehost, and it wasn't exactly fun trying to hunt down all the places that JSX could appear inside of a functional (or class based) component. Vue just has all of its HTML at the top of the `.vue` files.

As a comparison, here's the same component implemented with Vue ([see it on Codepen](https://codepen.io/brettfishy/pen/MWKLxpv)):

```html
<template>
  <div id="app">
    <section>
      <button @click="view = 'profile'">Profile</button>
      <button @click="view = 'followers'">Followers</button>
    </section>

    <section>
      <ul v-if="view === 'followers'">
        <li>Followers: {{ user.followers }}</li>
        <li>Following: {{ user.following }}</li>
      </ul>
      <ul v-else>
        <li>Name: {{ user.name }}</li>
        <li>Email: {{ user.email }}</li>
      </ul>
    </section>
  </div>
</template>

<script>
  export default {
    data: () => ({
      user: {
        name: 'John Doe',
        email: 'johndoe@example.com',
        followers: 1000,
        following: 500,
      },
      view: 'followers',
    }),
  };
</script>
```

Just looking at it, it feels so much cleaner. The JS is minimal, only containing the initial data. The best part is, all the HTML is in one place. No chance of JSX pieces randomly showing up in different parts of the render function. Yes, [I know you can use JSX with Vue](https://github.com/vuejs/jsx). But this seems more rare than common. In the year and a half timespan that I was working with Vue, almost every Stack Overflow post, documentation page, or blog post gave examples using the approach with the HTML template at the top followed by a `<script>` tag containing the logic. Most of the time you're probably going to see Vue code that follows the pattern above, and that's what I was used to and liked.

## So...why did I convert to React?

Reading that, it would be easy to wonder why I started to favor React over Vue when it came to choosing a framework for my personal projects. In the previous section, the example code I gave was small, but the Vue code at first glance just seems so much easier to grasp. The pros and cons mentioned above only compound with the large files and codebases I dealt with at the companies I worked for.

The BIGGEST reason why I ultimately started favoring React was that it seems so much easier to get TypeScript working with it. I mentioned this in my original article, but I don't think I stressed enough that if there were one reason why I've decided to stick with React, this would be it.

## React <3 TypeScript

As I started learning TypeScript, I started getting addicted to it because the type safety and additional Intellisense I got with my IDE felt _so good_. I won't go on about how great TypeScript is because there are already plenty of other articles on the internet about that. But basically, I started feeling kind of naked when working on normal JS projects. Especially when dealing with objects having more complex structures, I really started appreciating the cognitive load that TypeScript took away just because my IDE was able to tell me exactly which properties should exist on an object and what type they were.

Don't get me wrong, Vue's TS support has gotten to be pretty decent. I used to think that the official [class component decorators](https://github.com/vuejs/vue-class-component) were the only way to get decent TS support in Vue, which at first I wasn't a big fan of. I hadn't seen decorators in JS before, and I felt a little dirty using them since [they're not even officially part of JavaScript yet](https://github.com/tc39/proposal-decorators). I've since learned that class decorators are not a bad thing, especially since they make creating a TS GraphQL Express server insanely easy with the [TypeGraphQL library](https://github.com/MichalLytek/type-graphql).

I've since learned that class components are not a requirement for TS with Vue, since it can be as easy as using [Vue.extend](https://vuejs.org/v2/guide/typescript.html#Basic-Usage). And with Vue 3 natively supporting the [composition API](https://composition-api.vuejs.org/), using TypeScript in Vue will become even easier.

However, as I learned through experience, TS with Vue is by no means seamless. Using `Vue.extend` seems like the easiest way to get TS working with Vue without having to rewrite your code, but as [this article explains](https://medium.com/@toastui/developing-vue-components-with-typescript-18357ae7f297), there are basic problems with that. For example, you can't define prop types with interfaces, which I find to be a pretty big problem. To do that, you'll have to use the class components. Maybe there's a way around this now? If there is, feel free to correct me because I am not aware of it.

The downside with class components is that if you want to convert an existing Vue project to use TypeScript, you basically have to rewrite your whole component. With React, on the other hand, I've found it a lot easier to just "drop in" TypeScript.

Let's look at another example to illustrate this point. We'll create a simple component that could be used on a social media site - it will display information about a user and include a button allowing you to follow that user. It will accept everything it needs as props (making it easy to test :D). Say we originally created this component with ordinary Vue and wanted to convert it to use TypeScript. Here's the original ([Code Sandbox link](https://codesandbox.io/s/sweet-pine-wpd89?file=/src/App.vue)):

```html
<!-- UserProfile.vue -->
<template>
  <div>
    <h1>{{user.name}}</h1>
    <ul>
      <li>Username: {{user.username}}</li>
      <li>Followers: {{user.followers}}</li>
    </ul>
    <button @click="onFollow">Follow</button>
  </div>
</template>

<script>
  export default {
    name: 'UserProfile',
    props: {
      user: {
        type: Object,
        required: true,
      },
      onFollow: {
        type: Function,
        required: true,
      },
    },
  };
</script>
```

```html
<!-- App.vue -->
<template>
  <div id="app">
    <user-profile :user="user" :onFollow="onFollow" />
  </div>
</template>

<script>
  import UserProfile from './UserProfile.vue';

  export default {
    name: 'App',
    components: {
      UserProfile,
    },
    data: () => ({
      user: {
        name: 'John Doe',
        username: 'johndoe',
        followers: 1794,
      },
    }),
    methods: {
      onFollow() {
        alert(`You followed ${this.user.name}!`);
      },
    },
  };
</script>
```

Here's the TS version using class components ([Code Sandbox link](https://codesandbox.io/s/vue-typescript-example-syscs?file=/src/App.vue)):

```js
// types.ts
export interface User {
  name: string;
  username: string;
  followers: number;
}
```

```html
<!-- UserProfile.vue -->
<template>
  <div>
    <h1>{{user.name}}</h1>
    <ul>
      <li>Username: {{user.username}}</li>
      <li>Followers: {{user.followers}}</li>
    </ul>
    <button @click="onFollow">Follow</button>
  </div>
</template>

<script lang="ts">
  import { Component, Vue, Prop } from 'vue-property-decorator';
  import { User } from './types';

  @Component({
    name: 'UserProfile',
  })
  class UserProfile extends Vue {
    @Prop({ required: true }) user: User;
    @Prop({ required: true }) onFollow: () => void;
  }

  export default UserProfile;
</script>
```

```html
<!-- App.vue -->
<template>
  <div id="app">
    <user-profile :user="user" :onFollow="onFollow" />
  </div>
</template>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import { User } from './types';
  import * as UserProfile from './UserProfile.vue';

  @Component({
    name: 'App',
    components: {
      UserProfile,
    },
  })
  class App extends Vue {
    private user: User = {
      name: 'John Doe',
      username: 'johndoe',
      followers: 1794,
    };

    private onFollow(): void {
      alert(`You followed ${this.user.name}`);
    }
  }

  export default App;
</script>
```

As you can see, the difference between the two is fairly large. Because of the earlier problems mentioned with simply using `Vue.extend`, at this point using TypeScript with Vue requires either using class components, [the composition API plugin](https://github.com/vuejs/composition-api), or waiting for Vue 3 to come out so that the composition API is just built in. If you are rewriting an existing Vue codebase to use TypeScript, you'll basically have to completely change the structure of your Vue components. I experienced this while working on the website for my university. I originally used the offical options API, but decided to start using TypeScript as the data the site was handling became increasingly more complex.

I didn't necessarily have to rewrite my business logic, but for larger components, converting them to class components could take quite some time. I understood this was the price I had to pay to get type safety, and I accepted that. But now, many months later, as a React developer I can't help but think what the process would have been like if I were trying to convert an existing React site to use TypeScript.

Let's look at the same component from above but written in React. Here is it written with normal JS ([Code Sandbox](https://codesandbox.io/s/nice-chebyshev-4tgp8?file=/src/App.js)):

```js
import React, { useState } from 'react';

const UserProfile = ({ user, onFollow }) => {
  return (
    <div>
      <h1>{user.name}</h1>
      <ul>
        <li>Username: {user.username}</li>
        <li>Followers: {user.followers}</li>
      </ul>
      <button onClick={onFollow}>Follow</button>
    </div>
  );
};

export default function App() {
  const [user] = useState({
    name: 'John Doe',
    username: 'johndoe',
    followers: 1794,
  });

  const onFollow = () => {
    alert(`You followed ${user.name}!`);
  };

  return (
    <div className="App">
      <UserProfile user={user} onFollow={onFollow} />
    </div>
  );
}
```

Here's the same React app in TypeScript ([Code sandbox](https://codesandbox.io/s/late-platform-d3kwi?file=/src/App.tsx)):

```tsx
import React, { useState } from 'react';

interface User {
  name: string;
  username: string;
  followers: number;
}

interface UserProfileProps {
  user: User;
  onFollow: () => void;
}

const UserProfile = ({ user, onFollow }: UserProfileProps) => {
  return (
    <div>
      <h1>{user.name}</h1>
      <ul>
        <li>Username: {user.username}</li>
        <li>Followers: {user.followers}</li>
      </ul>
      <button onClick={onFollow}>Follow</button>
    </div>
  );
};

export default function App() {
  const [user] = useState<User>({
    name: 'John Doe',
    username: 'johndoe',
    followers: 1794,
  });

  const onFollow = () => {
    alert(`You followed ${user.name}!`);
  };

  return (
    <div className="App">
      <UserProfile user={user} onFollow={onFollow} />
    </div>
  );
}
```

Just like the Vue migration to TS, we needed to declare our types. But in React, that was pretty much all we had to do. Notice how similar the JS React and TS React apps are to each other. Granted, this is a pretty small example, but from experience I can say that it usually is this easy when migrating an existing React app to use TS. The other weekend, I decided to migrate my old JS React blog to use TS React, and it really was this easy. Basically all I had to do was add types where they were required, and I was done. No refactoring my code to use a new structure or decorators, the way I would have had to do in Vue.

Understand that this is not me saying that React is better than Vue. I'm just saying that I have had a much easier time using TypeScript with React, and that's a huge selling point because TypeScript is so important me. I get that this wouldn't be as big of a deal for a developer not using TypeScript.

In fact, if TypeScript didn't exist or if I only developed with normal JS, there's a good chance that I would prefer Vue! Hooks were a huge game changer with React, but I think just about every React developer (myself included) has run into headaches with infinite render loops because of messing up the dependencies in the `useEffect` hook. [This ESLint plugin](https://www.npmjs.com/package/eslint-plugin-react-hooks) helps find a lot of the trivial bugs associated with this problem and has saved my bacon on many occassions, but even with it, infinite render loops can happen. I've run into infinite render loops a couple of times with Vue, but it's definitely a lot more common in React. It's _really_ nice that Vue's `computed` and `watch`ed properties [figure out the dependencies for you](https://www.npmjs.com/package/eslint-plugin-react-hooks). I know this isn't _quite_ comparing the same thing, but they are pretty close. However, the ease of using TypeScript in React outweighs this problem for me, especially as I've gotten more experienced with using hooks and understanding their nuances.

## React has less secrets

In my original article, I said that React is just JavaScript, which is _sort of_ true. [The Vue website says so itself](https://vuejs.org/v2/guide/comparison.html#HTML-amp-CSS), but as many people commented to me, JSX is not valid JS, which is why we require something like Babel to build our JSX files. Yeah, [you don't _have_ to use JSX with React](https://reactjs.org/docs/react-without-jsx.html), but that doesn't sound like very much fun to me! That being said, React feels a lot closer to plain old JS than Vue does.

If you had told this to me when I first started learning React, I probably wouldn't have cared because I thought React was so much harder than Vue! But as I've spent more time with it, this feeling of React being so close to regular JS has grown on me.

For example, in a normal JS file, you usually have to `import` or `require` all your dependencies. React is no different. If you see an unfamiliar function or component in a React JSX file, you can just look at the `import` statement to see where it's coming from. Is it coming from a third party library, or from some other location in the project?

As an example, here's a tiny React app that uses some components from the [Material UI library](https://material-ui.com/) ([Code Sandbox link](https://codesandbox.io/s/exciting-merkle-xkn6f?file=/src/App.js)).

```js
import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';

export default function App() {
  const [items, setItems] = useState([]);
  const [text, setText] = useState('');

  const addItem = () => {
    setItems(prevItems => [...prevItems, text]);
    setText('');
  };

  return (
    <div className="App">
      <h1>My List of Things</h1>
      <ul>
        {items.map(item => (
          <li>{item}</li>
        ))}
      </ul>
      <TextField
        value={text}
        onChange={({ target: { value } }) => setText(value)}
        label="List item"
      />
      <Button variant="contained" onClick={addItem}>
        Add Item
      </Button>
    </div>
  );
}
```

The components we need from Material UI, such as `Button` and `TextField`, are just `import`ed at the top of the file. This is how it would be with pretty much every other React component library out there. Even if I'm working on a project that's using multiple third party libraries, every component, function, or constant can be traced pretty easily.

As a comparison, we'll look at the same component, only this time using [Vuetify](https://vuetifyjs.com/en/) ([Code Sandbox link](https://codesandbox.io/s/vuetify-template-ww8hd?file=/src/App.vue)).

```html
<template>
  <v-app>
    <h1>My List of Things</h1>
    <ul>
      <li v-for="(item, idx) in items" :key="idx">{{item}}</li>
    </ul>
    <v-container>
      <v-text-field v-model="text" label="List item" />
      <v-btn @click="addItem">Add Item</v-btn>
    </v-container>
  </v-app>
</template>

<script>
  export default {
    data: () => ({
      items: [],
      text: '',
    }),
    methods: {
      addItem() {
        this.items.push(this.text);
        this.text = '';
      },
    },
  };
</script>
```

These lines in our `main.js` actually make Vuetify available:

```js
import Vue from 'vue';
import Vuetify from 'vuetify';
Vue.use(Vuetify);
```

My main problem with this is that Vue allows Vuetify to make the v-\* components globally available (and I know that you can [manually import Vuetify components](https://vuetifyjs.com/en/customization/a-la-carte/#manually-importing) the way you have to do with Material UI). The main point I'm trying to get at is that it seems to be a common occurrence in Vue code to either have global components like in Vuetify or global variables available on `this`, such as `this.$router` or `this.$store` coming from Vue Router and Vuex, respectively. Yes, I know that you can just import the router and store objects instead of using these global variables, but in my experience with production code and online examples I've seen the global approach used more often. I'm not saying this is inherently a bad thing - it might not bother some people, and that's fine. In fact, a good IDE can help take some of the mystery out of finding the definition of these global components.

The main reason I don't like these global variables is it makes unit testing more difficult. I have had so many problems trying to get unit tests working with an app using Vuetify because the test runner complains about not being able to find the globally registered components. In the above example, in a unit test I would get errors about `v-app` or `v-container` not being defined. Even when following [Vuetify's guide on unit testing](https://vuetifyjs.com/en/getting-started/unit-testing/#unit-testing), I would still end up with weird errors and warnings from Jest that would take me far too long to fix. I never ran into problems like that with Material UI, because all the dependencies are just `import`ed, so Jest wouldn't complain about not being able to find them.

That's just one example, of course, but overall I've tended to just have better luck testing React apps than Vue apps. That's speaking from my own experience - someone else may have had better luck the other way around, and I'm not here to say that's wrong.

In summary of this point, when I say that React has less secrets, I mean that I've personally found it easier to figure out where a component's dependencies (third party or in-house) are coming from when working in large codebases. This has provided a lot of benefits. Testing, as I mentioned, is just one of them. Yes, lack of global components can make for a long list of `import` statements, I will admit. But it's always comforting to know that I can usually find out exactly where each piece of code in a React app is coming from. While working in a big Vue codebase, I found myself confused a lot by global variables on `this`. I thought it was too easy to get confused about if such variables were [instance properties](https://vuejs.org/v2/api/#Instance-Properties), coming from a third party plugin, or had been added to the Vue prototype somewhere else in the codebase. This was never a problem for me with React code.

## What about the weird JSX syntax?

Earlier, I mentioned that large React components at Bluehost confused me when JSX appeared in so many places throughout the component. To address this problem, I would argue that this isn't necessarily React's or JSX's fault. I believe that the source of these components' confusion came mostly from their size and not following basic principles of clean coding.

I formed this opinion after recently reading Bob Martin's book _Clean Code_. He gives several examples of large and confusing Java classes before proceeding to show how much more readable and maintainable they can be just by logically breaking them up into multiple classes. This same principle holds true with React and Vue components. When working as a Vue developer, I sometimes had to work with massive Vue files that other people had written, and I was just as confused as I was when working with other people's large React files.

At first I blamed my confusion on React, but I've learned that JSX appearing in multiple places hasn't been a problem for me as long as I keep my components small. Don't blame poorly written code on the framework.

## Conclusion

Once again, I'd like to reiterate that I don't believe Vue is bad - I still think it's really great, and I'm excitedly looking forward to the release of Vue 3. What I was hoping to get across by releasing this revised article was that my personal experiences as a web developer have shaped my decision to stick with React at this point in time.

I find React's TypeScript support to be the biggest selling point to me, as well as my experiences in writing unit tests for it. Maybe I was just doing something wrong that caused me so many struggles with getting Vue unit tests to work (especially with Vuetify), but while I enjoy writing tests, I don't enjoy spending too much time debugging them since I would rather be working on the app itself. In general, I've been more successful at accomplishing this by using React. Though Vue has treated me very well and I'd have no problem accepting a future job as a Vue developer, for my personal projects I'll be sticking with React.
