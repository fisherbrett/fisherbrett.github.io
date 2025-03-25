---
title: How to Test Responsive React Components
date: '2020-08-22T23:46:37.121Z'
layout: post
---

I was recently writing some responsive React components and needed to find a way to unit test them. I was using some custom components developed by my company that made it easy to render different layouts depending on the screen size. I wanted to test that certain components were visible on larger screen sizes and hidden on smaller screen sizes. I use Jest as my test runner, and I wasn't sure if there was a way to make Jest render different screen sizes. Luckily, it doesn't matter. There's a much easier way to test how your component behaves on different screen sizes.

As an example, let's create a simple responsive component. On small screen sizes it will print "I'm small!" and on larger screen sizes it will print "I'm big!". I'm going to use Material UI's [useMediaQuery](https://material-ui.com/components/use-media-query/) hook to determine what gets rendered based on the screen size. However, you'll soon see that it doesn't matter what library or method you use to make your app responsive.

Here's our first attempt: ([Code Sandbox](https://codesandbox.io/s/react-responsive-untestable-qkcbj?file=/src/App.js))

```js
import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import useMediaQuery from '@material-ui/core/useMediaQuery';

const App = () => {
  const theme = useTheme();
  const isSmall = useMediaQuery(theme.breakpoints.down('sm'));

  return <div>{isSmall ? "I'm small!" : "I'm big!"}</div>;
};

export default App;
```

What if I wanted to write a unit test that determined if the text "I'm small!" was rendered on small screens? That might be a little tricky. One solution would be to mock out `useMediaQuery`. The problem with that is it makes our unit tests flaky. What if in the future we decide to use a different method to determine the screen size? Then we would have to change our unit tests. Ideally our unit tests shouldn't need know about our components' implementation details.

I actually wrote about making your components more testable in [one of my previous posts](/better-testing). The principles I wrote about there can apply here as well. What if we just added another component that took `isSmall` as a prop? Then it would be easy to test. For example ([Code Sandbox](https://codesandbox.io/s/react-responsive-hknr3?file=/src/App.js)):

```js
import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import useMediaQuery from '@material-ui/core/useMediaQuery';

export const ResponsiveApp = ({ isSmall }) => (
  <div>{isSmall ? "I'm small!" : "I'm big!"}</div>
);

const App = () => {
  const theme = useTheme();
  const isSmall = useMediaQuery(theme.breakpoints.down('sm'));

  return <ResponsiveApp isSmall={isSmall} />;
};

export default App;
```

Now we could just write a unit test for `ResponsiveApp`, which doesn't have any dependencies like `useMediaQuery`. For example:

```js
import React from 'react';
import { render } from '@testing-library/react';
import { ResponsiveApp } from './App.jsx';

describe('ResponsiveApp test', () => {
  const createWrapper = isSmall => <ResponsiveApp isSmall={isSmall} />;

  it("displays I'm small! on small screens", () => {
    const { getByText } = createWrapper(true);
    expect(getByText("I'm small!")).toBeDefined();
  });

  it("displays I'm big! on big screens", () => {
    const { getByText } = createWrapper(false);
    expect(getByText("I'm big!")).toBeDefined();
  });
});
```

No mocking necessary! And if we change the method we use for determining responsive behavior in `App`, it won't affect our unit test at all. This is a small example, but following this kind of pattern has changed how I write code and makes components so much easier to test.
