---
title: How to Create Your Own React Text Field
date: '2020-08-15T23:46:37.121Z'
layout: post
---

[On the home page of my blog](https://brettfisher.dev), there is a search field that lets you search for posts by title or tags. I originally tried using [Material UI's Text Field component](https://material-ui.com/components/text-fields/#text-field), which seemed to be working just fine. However, once I built my site and ran it in production mode, the styling on the Text Field disappeared. I don't know if this is a problem with Material UI or Gatsby (or even something else), but I wasn't about to publish that to my site. All I wanted was a simple input element with some nice styling. I thought, "Hey, I'm a web developer. I'll just make the component myself"! I'll show you how I did it.

I'll be using React with TypeScript. If you want to follow along, I suggest either [creating a new Gatsby site](https://www.gatsbyjs.com/docs/quick-start/), which comes with TypeScript support out of the box, or [adding TypeScript to a Create React App project](https://create-react-app.dev/docs/adding-typescript/). I'll be using Tailwind CSS to style my components, so you'll also want to [install that](https://tailwindcss.com/docs/installation).

## Create a Basic `input` Wrapper

My goal was to just create a simple search field, or a generic text field that I could use in other places on my site. HTML's `input` field works just fine, but we'll need to style it a bit so that it looks nice. First, create a `TextField.tsx` file that just wraps a basic `input` element:

[Code Sandbox](https://codesandbox.io/s/react-text-field-0dvft?file=/src/TextFieldBasicWrapper.tsx)

```tsx
import React from 'react';

const TextField = () => {
  return <input />;
};

export default TextField;
```

Test it out in your App.tsx and it should just render a normal `input` field. Ok, it works, but it's not very useful. Let's add props for `value` and `onChange` so we can observe and manipulate the Text Field's state.

[Code Sandbox](https://codesandbox.io/s/react-text-field-0dvft?file=/src/TextFieldWithState.tsx)

```tsx
import React from 'react';

interface TextFieldProps {
  value: string;
  onChange: (val: string) => void;
}

const TextField = ({ value, onChange }: TextFieldProps) => {
  return (
    <input
      value={value}
      onChange={({ target: { value } }) => onChange(value)}
    />
  );
};

export default TextField;
```

Notice that `input`'s default `onChange` event accepts a callback where the first argument is the input event. I'm not too interested in that, so I destructured that event and just pass in the `value` to the `onChange` callback. It just simplifies things a bit. Great, now we have a basic `input` wrapper! Let's work on styling it.

## Styling our Text Field

If you haven't used Tailwind before, then it basically just provides a set of utility classes that easily let you style your components. I highly recommend [checking it out](https://tailwindcss.com/).

Add the following `className` to your `input` component:

[Code Sandbox](https://codesandbox.io/s/react-text-field-0dvft?file=/src/TextFieldStyled.tsx)

```html
<input className="rounded-md w-full border border-gray-400 p-3 mb-5" ... />
```

These are Tailwind classes that round the corners on the `input`, give it a light gray border, add some padding and bottom margin, and makes the input the full width of its parent. These are just my personal preferences for a generic Text Field component - feel free to style yours however you want!

## Adding More Useful Props

Our Text Field is looking great. But it would be nice to be able to modify other important values on the underlying `input` element, such as `placeholder`, `autoFocus`, `name`, and `type`. Adding those in as props is pretty easy:

[Code Sandbox](https://codesandbox.io/s/react-text-field-0dvft?file=/src/TextFieldWithMoreProps.tsx)

```tsx
import React from 'react';

interface TextFieldProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  autoFocus?: boolean;
  name?: string;
  type?: 'email' | 'password' | 'text';
}

const TextField = ({ onChange, ...rest }: TextFieldProps) => {
  return (
    <input
      className="rounded-md w-full border border-gray-400 p-3 mb-5"
      onChange={({ target: { value } }) => onChange(value)}
      {...rest}
    />
  );
};

export default TextField;
```

Notice that I decided to only destructure `onChange` because I use it a little differently than the way `input` does. All the other props are stored in `rest` because then they can be directly passed to `input` with the spread operator.

## Doubling our Text Field as a `textarea`

I'll add in one more prop called `textarea`. If it's true, it will make our Text Field render a `textarea` instead of an `input`. This is simpler to do than creating a custom Textarea component because all the props we are passing to `input` can also be passed to `textarea`.

[Code Sandbox](https://codesandbox.io/s/react-text-field-0dvft?file=/src/TextFieldWithTextarea.tsx)

```tsx
import React from 'react';

type InputElement = HTMLInputElement | HTMLTextAreaElement;
type InputChangeEvent = React.ChangeEvent<InputElement>;

interface TextFieldProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  autoFocus?: boolean;
  name?: string;
  type?: 'email' | 'password' | 'text';
  textarea?: boolean;
}

const TextField = ({ onChange, textarea = false, ...rest }: TextFieldProps) => {
  const InputElement = textarea ? 'textarea' : 'input';
  return (
    <InputElement
      className={`rounded-md w-full border border-gray-400 p-3 mb-5 ${
        textarea ? 'h-32' : ''
      }`}
      onChange={({ target: { value } }: InputChangeEvent) => onChange(value)}
      {...rest}
    />
  );
};

export default TextField;
```

There are a few important changes here. First take a look at the variable called `InputElement`. If the `textarea` is true, then our component will render a `textarea`. Otherwise, it will render a normal `input`.

Next, take a look at the `className` property. I wasn't satisfied with the height of the default `textarea`, so I conditionally added an `h-32` class if the `textarea` prop is true. That just makes its height a little bigger.

Finally, take note of the `onChange` prop. Since our component can render either a `textarea` or an `input`, TypeScript got confused about the type of the `value` variable in the `onChange` callback. I created these two types at the top of the file:

```ts
type InputElement = HTMLInputElement | HTMLTextAreaElement;
type InputChangeEvent = React.ChangeEvent<InputElement>;
```

I just figured these out with my editor's intellisense. Now when I add the `InputChangeEvent` as the type annotation for the parameter in our `onChange` callback, TypeScript stops complaining.

## Passing a Ref to our Text Field

So far, our custom Text Field is working out pretty well. The last feature I'd like is to be able to pass a ref to the underlying `input` element. This would be useful if we wanted to programatically focus the `input`, for example. Luckily this is pretty easy to do with React's [ref forwarding feature](https://reactjs.org/docs/forwarding-refs.html). Pretty much all we have to do is wrap our functional component in a call to `React.forwardRef`.

[Code Sandbox](https://codesandbox.io/s/react-text-field-0dvft?file=/src/TextFieldWithRef.tsx)

```tsx
import React from 'react';

type InputElement = HTMLInputElement | HTMLTextAreaElement;
type InputChangeEvent = React.ChangeEvent<InputElement>;

interface TextFieldProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  autoFocus?: boolean;
  name?: string;
  type?: 'email' | 'password' | 'text';
  textarea?: boolean;
}

const TextField = React.forwardRef<InputElement, TextFieldProps>(
  ({ onChange, textarea = false, ...rest }, ref) => {
    const InputElement = textarea ? 'textarea' : 'input';
    return (
      <InputElement
        ref={ref as any}
        className={`rounded-md w-full border border-gray-400 p-3 mb-5 ${
          textarea ? 'h-32' : ''
        }`}
        onChange={({ target: { value } }: InputChangeEvent) => onChange(value)}
        {...rest}
      />
    );
  }
);

export default TextField;
```

Now if a ref is given to Text Field, it will apply directly to the `input` or `textarea` component. The only way I was able to get TypeScript to stop complaining was to put `ref={ref as any}`, which isn't ideal but I wasn't too concered about it since I'm the only one who will be using this component. If you know how to give it a proper type, please let me know!

## Conclusion

That's about all there is to creating a custom Text Field. While I love Material UI, it's a fun exercise to see if I can create components on my own. Plus, I still haven't figured out why Material UI has problems with its Text Field on my built site...anyways, happy coding!
