---
title: The Easiest Way to Use Query Parameters in React
date: '2020-09-20T23:46:37.121Z'
layout: post
---

**TLDR;** - I wrote a hook that makes it easy to manage URL query parameters with React. View it on [Github](https://github.com/bandrewfisher/use-query-param) or [Code Sandbox](https://codesandbox.io/s/use-query-param-9fnnw?file=/src/App.tsx).

There have been multiple times I've been working on projects and have needed to get and set query parameters in the URL. I tried watching the URL with `useEffect`, but that led to way too many bugs and messy code. Eventually, I decided to create a simple hook that would take away all the pain of getting and setting query parameters!

I put all this code in a file in my projects and just import it whenever I need to use it. In fact, you can just copy and paste the following code block to immediately simplify query parameter management in your own project!

```js
// useQueryParam.ts

import { useState } from 'react';

const getQuery = () => {
  if (typeof window !== 'undefined') {
    return new URLSearchParams(window.location.search);
  }
  return new URLSearchParams();
};

const getQueryStringVal = (key: string): string | null => {
  return getQuery().get(key);
};

const useQueryParam = (
  key: string,
  defaultVal: string
): [string, (val: string) => void] => {
  const [query, setQuery] = useState(getQueryStringVal(key) || defaultVal);

  const updateUrl = (newVal: string) => {
    setQuery(newVal);

    const query = getQuery();

    if (newVal.trim() !== '') {
      query.set(key, newVal);
    } else {
      query.delete(key);
    }

    // This check is necessary if using the hook with Gatsby
    if (typeof window !== 'undefined') {
      const { protocol, pathname, host } = window.location;
      const newUrl = `${protocol}//${host}${pathname}?${query.toString()}`;
      window.history.pushState({}, '', newUrl);
    }
  };

  return [query, updateUrl];
};

export default useQueryParam;
```

Using it in components is easy ([Code Sandbox](https://codesandbox.io/s/use-query-param-9fnnw)):

```js
import React from 'react';
import useQueryParam from './useQueryParam';

const App = () => {
  const [search, setSearch] = useQueryParam('search', '');

  return (
    <input
      value={search}
      onChange={({ target: { value } }) => setSearch(value)}
    />
  );
};
```

That's it! `useQueryParam` takes two arguments - the first is the name of the parameter, and the second is the default value to be assigned in case the parameter is not present in the URL. If you were just looking for an easy way to manage query parameters in React, you can stop reading. Just copy the code block above and you're good to go. If you'd like to know a little more about how it works, then keep reading.

## How it Works

Let's look at the first two functions:

```js
const getQuery = () => {
  if (typeof window !== 'undefined') {
    return new URLSearchParams(window.location.search);
  }
  return new URLSearchParams();
};

const getQueryStringVal = (key: string): string | null => {
  return getQuery().get(key);
};
```

`getQuery` just returns an instance of [URLSearchParams](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams), which just contains a mapping of URL query names to their respective values. Note that for use with SSRs like Gatsby, you must check for the existence of `window`.

`getQueryStringVal` just gets the value of a specific parameter in the URL. We can use these two functions to craft the actual `useQueryParam` hook. It's got two parts, let's examine those. Here's the first part at the beginning of the hook:

```js
const [query, setQuery] = useState(getQueryStringVal(key) || defaultVal);
```

We use our `getQueryStringVal` to get the value of the query parameter, and initialize `query` to `defaultVal` in case `key` doesn't exist in the URL. This will store the value of the parameter, now we just need a function to update it:

```js
const updateUrl = (newVal: string) => {
  setQuery(newVal);

  const query = getQuery(); // Get the URLSearchParams object

  // Update URLSearchParams object
  if (newVal.trim() !== '') {
    query.set(key, newVal);
  } else {
    query.delete(key);
  }

  // This check is necessary if using the hook with Gatsby
  if (typeof window !== 'undefined') {
    // Update URL
    const { protocol, pathname, host } = window.location;
    const newUrl = `${protocol}//${host}${pathname}?${query.toString()}`;
    window.history.pushState({}, '', newUrl);
  }
};
```

This is the function we return from the hook for updating the URL. We first update the variable we created with `useState`. We then use the `set` method on `URLSearchParams` to update the mapping. Finally, we use the [pushState](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState) function on `window.history` to update the URL without the page refreshing.

That's it! This hook may not necessarily address every possible edge case that could come up when working with query parameters. However, it's worked great for me so far. Feel free to use it in your own projects!
