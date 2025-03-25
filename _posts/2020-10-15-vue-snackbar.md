---
title: The Easiest Way to Use Snackbars in Vue
date: '2020-10-15T23:46:37.121Z'
layout: post
---

**TLDR**; Check out the code on [Code Sandbox](https://codesandbox.io/s/snackbar-7e0jq) to learn how to make a snackbar that can be opened from any Vue component in your app!

In one of my Vue projects, I display a simple popup ("snackbar") explaining any errors that get thrown. I started to find myself adding a snackbar to every component that could possibly throw an error (such as from a network call). On top of that, I had to add data members controlling the visibility of the snackbar and the message it displayed.

This article explains how to create a single snackbar that you can then open from any component with any message you want. This eliminates any duplicate snackbar code across components. Let's get started!

## Step 1: Create the event bus

To make a snackbar that can be opened across the entire app, we'll use a pattern called an event bus. An event bus is a global object that can receive and respond to events. Inside our Vue components, we can add a snackbar event to the bus and have it respond by opening a snackbar.

Lucky for us, we can just use a new Vue object to function as an event bus. It provides the handy `$emit` and `$on` functions to emit and respond to events.

```js
// EventBus/index.js

import Vue from 'vue';

export const ACTIONS = {
  SNACKBAR: 'snackbar',
};

const EventBus = new Vue();

export default EventBus;
```

That's it! For convenience, I also added an `ACTIONS` object that makes it easy to constrain the actions that can be emitted on the bus.

## Step 2: Create a function to open the snackbar

I created a folder called `globalActions` with an `index.js` file to contain functions that could be used in any component across my app. Let's put a function in there that will add the snackbar event to the event bus:

```js
// globalActions/index.js

import EventBus, { ACTIONS } from '../EventBus/index';

export const showSnackbar = message => {
  EventBus.$emit(ACTIONS.SNACKBAR, message);
};
```

Now let's create a component that uses this function to display a snackbar.

## Step 3: Use the function in a component

I created a custom component called `MyComponent` to use this snackbar function:

```html
<!-- components/MyComponent.vue -->
<template>
  <v-btn @click="openSnackbar">Show snackbar</v-btn>
</template>

<script>
  import { showSnackbar } from '../globalActions';
  export default {
    methods: {
      openSnackbar: () => {
        showSnackbar('Hello from snackbar!');
      },
    },
  };
</script>
```

This imports the `showSnackbar` function and calls it with the message "Hello from snackbar!" when a button is pressed. Right now we won't see a snackbar because all that will happen is an event gets emitted on the event bus. Now let's tell the event bus that when it sees the `ACTIONS.SNACKBAR` event, it should show a snackbar. We'll add this to our `App.vue` file so that any component will be able to display a snackbar.

## Step 4: Add a snackbar to App.vue

I'm using Vuetify in my project, so it's really easy to just pop in [Vuetify's snackbar](https://vuetifyjs.com/en/components/snackbars/). However, you can easily accomplish the same goal with any other library or even your own custom snackbar. I just have one snackbar component in `App.vue` and some data members to control its visibility and the message it displays:

```html
<!-- App.vue -->
<template>
  <div id="app">
    <my-component />
    <v-snackbar v-model="snackbar" timeout="2500"
      >{{ snackbarMessage }}</v-snackbar
    >
  </div>
</template>

<script>
  import EventBus, { ACTIONS } from './EventBus/index';
  import MyComponent from './components/MyComponent.vue';

  export default {
    name: 'App',
    components: {
      MyComponent,
    },
    data: () => ({
      snackbar: false,
      snackbarMessage: '',
    }),
    mounted() {
      EventBus.$on(ACTIONS.SNACKBAR, message => {
        this.snackbarMessage = message;
        this.snackbar = true;
      });
    },
  };
</script>
```

When the component is mounted, we use the `$on` function on our event bus to listen to the `ACTIONS.SNACKBAR`. It updates the `snackbarMessage` member and sets `snackbar` to true. Now whenever we call the `showSnackbar` function from a component, a snackbar will pop up with the passed-in message!

Check out the full code on [Code Sandbox](https://codesandbox.io/s/snackbar-7e0jq).

## Conclusion

An event bus provides a super easy way to respond to events that could happen at any place in our app. You can also customize the snackbar as much as you want since the message it displays doesn't have to be the only argument you pass to the bus. For example, you could pass in options for the snackbar color, the duration it stays open, or a callback function to perform when the snackbar is clicked.

That's it for today, happy snackbar-ing!
